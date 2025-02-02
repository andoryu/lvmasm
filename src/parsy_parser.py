from dataclasses import dataclass
import enum
from pprint import pprint
import re

from parsy import eof, from_enum, regex, seq


#-------------------
# AST nodes

class Opcode(enum.Enum):
    PUSHI32 = "pushi32"
    PUSHF32 = "pushf32"
    ADDI    = "addi"
    ADDF    = "addf"
    POP     = "pop"

@dataclass
class Integer:
    value: int

@dataclass
class Real:
    value: float

@dataclass
class Label:
    value: str

@dataclass
class String:
    value: str


#----------------------------------
# parsers

space = regex(r"\s+").desc("white space")
padding = regex(r"\s*").desc("padding")
eol = regex(r"\s*\n").desc("eol").result(None)
comment = regex(r"\s*;[^\n]*").desc("comment")

label = regex(r"(\w+):", group=1).desc("label").map(Label)
int_val = regex(r"\d+").desc("integer").map(int).map(Integer)
str_val = regex(r'"[^"\n]*"').desc("string").map(lambda s: String(s[1:-1])).map(String)
flt_val = regex(r"[+-]?(\d+)(\.\d+)?\s*([eE][+-]?\d+)?").desc('float').map(float).map(Real)
opcode = from_enum(Opcode).desc("opcode")

argument = int_val | str_val | flt_val

instruction = seq(opcode, space >> argument) | opcode

labeled_instruction = seq(
    label,
    space >> instruction
)

line =  comment << eol | \
        padding >> instruction << eol | \
        padding >> instruction << comment << eol | \
        padding >> label << eol | \
        padding >> label << comment << eol | \
        seq(padding >> label, space >> instruction << eol) | \
        seq(padding >> label, space >> instruction << comment << eol) | \
        (eof | eol)

asm_parser = line.many()

if __name__ == "__main__":
    # testing parsers
    print("space '    ':", space.parse("   "))
    print("padding '    ':", padding.parse("   "))
    print("padding '':", padding.parse(""))
    print("eol:", eol.parse("\n"))

    print("comment:", comment.parse(";this is a comment"))

    print("label:", label.parse("label:"))
    print("integer:", int_val.parse("1234"))
    print("string:", str_val.parse('"test string"'))
    print("float1:", flt_val.parse("0.0"))
    print("float2:", flt_val.parse("+3.14159"))
    print("float3:", flt_val.parse("1.0E-5"))
    print("float4:", flt_val.parse("1E08"))
    print("float5:", flt_val.parse("+3E+08"))
    print("float6:", flt_val.parse("+3.14159e+0"))

    print("opcode:", opcode.parse("pushi32"))
    print("opcode:", opcode.parse("pop"))

    print("argument, int:", argument.parse("5678"))
    print("argument. str:", argument.parse('"this is a test"'))
    print("argument, flt:", argument.parse("+3.14159e+0"))

    print("instruction1:", instruction.parse("pushi32 1234"))
    print("instruction2:", instruction.parse("pop"))

    print("labeled_instruction:", labeled_instruction.parse("label2: pop"))

    print("")

    print("line1", line.parse("  ;this is a comment\n"))
    print("line1a", line.parse(" \n"))
    print("line2", line.parse("pushi32 1024\n"))
    print("line2a", line.parse("  pushi32 1024\n"))
    print("line3", line.parse("  label:\n"))
    print("line4", line.parse("label2: addi\n"))
    print("line4a", line.parse("label2: addi ; testing 123\n"))
    print("line5", line.parse("pop ; test comments\n"))
    print("line6", line.parse("pop\n"))

    print("\nAsm by line")
    print("line1", line.parse("; opening comment\n"))
    print("line2", line.parse("main:  ;this is main\n"))
    print("line2a", line.parse("  \n"))
    print("line3", line.parse("    pushi32 200     ; push 200 on stack\n"))
    print("line4", line.parse("    pushi32 100     ; push 100 on stack\n"))
    print("line5", line.parse("    addi            ; add integers\n"))
    print("line6", line.parse("    pop             ; pop the result\n"))
    print("line7", line.parse("\n"))

    print("\nAsm file:")
    test_asm = r"""
    ; opening comment
    main:

        pushi32 200     ; push 200 on stack
        pushi32 100     ; push 100 on stack
        addi            ; add integers
        pop             ; pop the result
    """
    pprint(asm_parser.parse(test_asm))
