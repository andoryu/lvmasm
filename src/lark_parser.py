from pprint import pprint

from lark import Lark

test_asm = r"""
.data
; opening comment
.code
main:               ; this is main

    pushi32 +200     ; push 200 on stack
    pushi32 -100     ; push 100 on stack
    addi            ; add integers
    pop             ; pop the result

area_circle:
    pushf32 3.14159
    pushf32 14.6E-03
    squaref
    mulf32
    pop

"""


asm_grammar = r"""
program: data_section? code_section

argument: INT | FLOAT

instruction: LABEL? OPCODE
    | LABEL? OPCODE argument

code_section: ".code" instruction+
data_section: ".data"

OPCODE: "pushi32" | "pushf32"
        | "addi" | "subi" | "muli" | "divi" | "modi" | "expi"
        | "addf" | "subf" | "mulf" | "divf" | "modf" | "expf"
        | "squarei" | "squaref" | "sqrooti" | "sqrootf"
        | "pop"

LABEL: /[a-zA-Z_][\w_]+:/

COMMENT: /;[^\n]*/

INT: ["+"|"-"]? UINT
FLOAT: ["+"|"-"]? UFLOAT

%import common.WS
%import common.INT -> UINT
%import common.FLOAT -> UFLOAT
%import common.NEWLINE

%ignore WS
%ignore NEWLINE
%ignore COMMENT
"""

if __name__ == "__main__":
    parser = Lark(asm_grammar, start="program")

    res = parser.parse(test_asm)
    print(res.pretty())
