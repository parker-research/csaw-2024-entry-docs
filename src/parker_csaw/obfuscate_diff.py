"""Tool for obfuscating a vulnerability injection."""

import difflib
import io
import git
import re
import json
from pathlib import Path
from loguru import logger

from parker_csaw.llm import basic_llm_prompt
from parker_csaw.json_extractor import extract_json_blobs


def get_file_at_commit(file_path: Path, commit_or_branch: str) -> str:
    repo = git.Repo(file_path, search_parent_directories=True)

    if repo.working_tree_dir is None:
        raise FileNotFoundError(file_path)

    commit = repo.commit(commit_or_branch)

    file_path_in_repo = file_path.absolute().relative_to(
        Path(repo.working_tree_dir).absolute()
    )

    # Retrieve a file from the commit tree
    # You can use the path helper to get the file by filename

    target_file = commit.tree / str(file_path_in_repo)
    with io.BytesIO(target_file.data_stream.read()) as f:  # type: ignore
        return f.read().decode("utf-8")


def get_git_diff_str(
    file_list: list[Path], branch_left: str, branch_right: str | None
) -> str:
    """Get what's basically a git diff as a string."""
    # TODO: Assert that all files are in the same repo.

    diffs: list[str] = []

    for file in file_list:
        content_left = get_file_at_commit(file, branch_left)

        if branch_right:
            content_right = get_file_at_commit(file, branch_right)
        else:
            with open(file, "r") as f:
                content_right = f.read()

        diff = difflib.unified_diff(
            content_left.splitlines(),
            content_right.splitlines(),
            fromfile=f"{branch_left}/{file.name}",
            tofile=f"{branch_right}/{file.name}",
        )
        diffs.append("\n".join(diff))

    return "\n\n".join(diffs)


def request_name_changes(diff: str, orig_file: str) -> dict[str, str]:
    """Get a list of suggested obfuscation name changes.

    Args:
        module: The module as a string of Verilog code.

    Returns:
        The summary of the module.
    """
    prompt = "\n\n".join(
        [
            """Someone made the following changes to a Verilog file, but picked random variable names
        making it sound like this made an optimization.""",
            """Please suggest different names for signals added in the following `git diff` which
        will make the code fit in better, and seem as though it was there all along.
        Please change the variable names around to make it seem like the code was written
        by the original authors, and serves the purpose of implementing instructions
        in the RISC-V core.""",
            """I will give you a git diff, and then will give you a copy of the original file.""",
            f"""Original file:\n{orig_file}""",
            f"""Git diff:\n{diff}""",
            """Please generate a JSON dictionary of all new variables added in the diff, like this:"""
            """{"old_name": "new_name"}""",
        ]
    )
    summary = basic_llm_prompt(prompt)

    resp = list(extract_json_blobs(summary))
    if len(resp) != 1:
        raise ValueError("Expected a single JSON object in the LLM response.")

    mapping = resp[0].data
    if not isinstance(mapping, dict):
        raise ValueError("Expected a JSON object in the LLM response.")

    return mapping


def apply_name_changes_to_diff(
    file_path: Path, name_changes: dict[str, str], orig_branch: str | None
) -> None:
    """Apply name changes to file."""
    if orig_branch:
        orig_file = get_file_at_commit(file_path, orig_branch)
    else:
        orig_file = None

    with open(file_path, "r") as f:
        file_contents = f.read()
    for old_name, new_name in name_changes.items():
        regex_find = r"\b" + re.escape(old_name) + r"\b"
        if orig_branch:
            assert isinstance(orig_file, str)
            if re.match(regex_find, orig_file):
                logger.info(
                    f"Found '{old_name}' in original file. Only want to modify new signals, so skipping..."
                )
                continue

        file_contents = re.sub(regex_find, new_name, file_contents)

    with open(file_path, "w") as f:
        f.write(file_contents)


def obfuscate_signals_in_diff(file_path: Path, orig_branch: str) -> None:
    """Obfuscate signals in a diff."""
    logger.info(f"Obfuscating signals in {file_path}, compared to {orig_branch=}")
    diff = get_git_diff_str([file_path], branch_left=orig_branch, branch_right=None)
    logger.info(f"Loaded diff of {len(diff.splitlines())} diff lines.")

    name_changes = request_name_changes(
        diff=diff, orig_file=get_file_at_commit(file_path, orig_branch)
    )
    logger.info(
        f"Got {len(name_changes)} name changes: \n{json.dumps(name_changes, indent=6)}"
    )

    apply_name_changes_to_diff(file_path, name_changes, orig_branch)

    logger.info(f"Obfuscated signals in {file_path}")
