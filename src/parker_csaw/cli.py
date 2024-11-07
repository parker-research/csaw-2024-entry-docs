from pathlib import Path

from loguru import logger
import typed_argparse as tap

from parker_csaw.summarize_modules import summarize_modules_at_path


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
