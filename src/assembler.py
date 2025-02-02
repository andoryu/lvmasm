import argparse
from pathlib import Path

# from parsy import

import parser

def assemble(source, output):

    asm_parser = parser.asm()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source_file", required=True,
        help="Source assembly file")

    parser.add_argument("-o", "--output_file", default="out.bin",
        help="output binary file")

    args = parser.parse_args()

    source = Path(args.source_file)
    if not source.exists():
        print("Unable to find source file at", args.source_file)

    output = Path(args.output_file)
    if not Path(output.parent).exists():
        print("Output path does not exist", output.parent)

    assemble(source, output)

if __name__ == "__main__":
    main()
