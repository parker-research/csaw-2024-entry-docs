from pathlib import Path

from loguru import logger
import typed_argparse as tap

from parker_csaw.summarize_modules import (
    split_verilog_file_into_modules,
    summarize_module,
)


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

# Argument parsing setup
class SummarizeModulesArgs(tap.TypedArgs):
    input_path: Path = tap.arg(
        positional=True, help="Path to a folder or file to summarize Verilog modules."
    )
    output_folder_path: Path = tap.arg(
        positional=True, help="Path to a folder to write the module summaries to."
    )


def run_summarize_modules(args: SummarizeModulesArgs):
    summarize_modules_at_path(args.input_path, args.output_folder_path)
    logger.info("Done summarizing modules.")


def main() -> None:
    tap.Parser(
        tap.SubParserGroup(
            tap.SubParser(
                "summarize-modules",
                SummarizeModulesArgs,
                help="Help of bar",
            ),
        ),
    ).bind(
        run_summarize_modules,
    ).run()


if __name__ == "__main__":
    main()
