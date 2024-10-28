from pathlib import Path
from typing import Any

import git
import yaml


def get_repo_root() -> Path:
    """Gets the root of the repository."""
    repo_root_str = git.Repo(__file__, search_parent_directories=True).working_tree_dir
    assert repo_root_str is not None
    repo_root = Path(repo_root_str)
    return repo_root


def get_secrets() -> dict[str, Any]:
    """Loads the secrets from the secrets file.

    Returns:
        The secrets.
    """
    secrets_file = get_repo_root().rglob("**/secrets.yml")

    if not secrets_file:
        raise FileNotFoundError("Secrets file not found.")

    secrets_file = list(secrets_file)[0]
    with open(secrets_file) as f:
        return yaml.safe_load(f)


def get_openai_api_key() -> str:
    return get_secrets()["api_key"]
