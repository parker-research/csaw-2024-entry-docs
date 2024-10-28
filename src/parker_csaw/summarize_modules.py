"""A script which creates a summary document of each of the modules, by prompting an LLM."""

import re

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
