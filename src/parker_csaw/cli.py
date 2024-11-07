from pathlib import Path

from loguru import logger
import typed_argparse as tap

from parker_csaw.summarize_modules import summarize_modules_at_path
from parker_csaw.obfuscate_diff import obfuscate_signals_in_diff


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


class ObfuscateDiffArgs(tap.TypedArgs):
    input_file: Path = tap.arg(positional=True, help="Path to a file to obfuscate.")
    original_branch: str = tap.arg(
        positional=True, help="Branch or commit to compare against, before injection."
    )


def run_obfuscate_diff(args: ObfuscateDiffArgs):
    obfuscate_signals_in_diff(args.input_file, args.original_branch)
    logger.info("Done obfuscating diff.")


def main() -> None:
    # Guide: https://typed-argparse.github.io/typed-argparse/high_level_api/#sub-commands
    tap.Parser(
        tap.SubParserGroup(
            tap.SubParser(
                "summarize-modules",
                SummarizeModulesArgs,
                help="Summarize Verilog modules into a single Markdown file.",
            ),
            tap.SubParser(
                "obfuscate",
                ObfuscateDiffArgs,
                help="Obfuscate the signals in a file, based on the diff from a previous unchanged commit.",
            ),
        ),
    ).bind(
        run_summarize_modules,
        run_obfuscate_diff,
    ).run()


if __name__ == "__main__":
    main()
