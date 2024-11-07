"""A script which creates a summary document of each of the modules, by prompting an LLM."""

import re
from pathlib import Path

from loguru import logger

from parker_csaw.llm import basic_llm_prompt


def split_verilog_file_into_modules(verilog: str) -> dict[str, str]:
    """Splits a Verilog file into modules.

    Args:
        verilog: The Verilog file as a string.

    Returns:
        A dictionary where the keys are the module names and the values are the module contents.
    """
    module_lines: dict[str, list[str]] = {}

    module_name = None
    for line in verilog.splitlines():
        match = re.match(r"module (\w+)", line)
        if match:
            module_name = match.group(1)
            module_lines[module_name] = []

        # Skip lines at the start.
        if module_name is None:
            continue

        module_lines[module_name].append(line)
        if line.strip() == "endmodule":
            module_name = None

    return {
        module_name: "\n".join(lines) for module_name, lines in module_lines.items()
    }


def summarize_module(module: str) -> str:
    """Summarizes a module.

    Args:
        module: The module as a string of Verilog code.

    Returns:
        The summary of the module.
    """
    summary = basic_llm_prompt(
        "You are a helpful Verilog designer. This module is part of a RISC-V core. Please summarize this module in about 3 sentences:\n"
        + module
    )

    return summary


def summarize_modules_at_path(input_path: Path, output_folder_path: Path) -> None:
    """Summarize modules, writing them to output_folder_path."""

    if input_path.is_dir():
        input_file_list = list(input_path.rglob("*.v")) + list(input_path.rglob("*.sv"))
    else:
        input_file_list = [input_path]

    input_file_list.sort()

    output_summary_md = ""

    for input_file_path in input_file_list:
        _output_folder_path = (
            output_folder_path
            / input_file_path.relative_to(input_path).parent
            / (input_file_path.stem + input_file_path.suffix.replace(".", "_"))
        )
        _output_folder_path.mkdir(parents=True, exist_ok=True)
        logger.info(
            f"Writing modules from {input_file_path.name} to {_output_folder_path}"
        )

        modules = split_verilog_file_into_modules(input_file_path.read_text())
        for module_name, module_verilog in modules.items():
            # Write out the module itself.
            (_output_folder_path / f"{module_name}").with_suffix(
                input_file_path.suffix
            ).write_text(module_verilog)

            # Write out the summary.
            summary = summarize_module(module_verilog)
            (_output_folder_path / f"{module_name}.summary.txt").write_text(summary)

            output_summary_md += f"## `{input_file_path.relative_to(input_path)}` -> `{module_name}` Module\n\n"

            output_summary_md += f"{summary}\n\n"

            # If the module is small enough, include it in the summary.
            if len(module_verilog) < 500:
                output_summary_md += f"```verilog\n{module_verilog}\n```\n\n"

    (output_folder_path / "summary.md").write_text(output_summary_md)
