import argparse
from pathlib import Path

import binary
import parser

def make_ast(lark_tree):
    print(lark_tree.pretty())


def assemble(source, output):

    asm_parser = parser.create_parser()

    #parse into the Lark parse tree
    with source.open("r") as fh:
        asm_source = fh.read()
        lark_tree = asm_parser.parse(asm_source)

    print(lark_tree.pretty())

    #TODO arity and type checks

    #create the binary format
    binary.build_binary(lark_tree)


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
