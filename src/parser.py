from dataclasses import dataclass
import enum

from parsy import from_enum, regex


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


#----------------------------------
# parsers
def asm():
    comment = regex(r"\s*;[^\n]\n")

    label = regex(r"(\w+):").map(Label)
    integer = regex(r"\d+").map(int).map(Integer)
    opcode = from_enum(Opcode)

    argument = integer()

    instruction = label.optional().opcode().argument()

    line = comment() | instruction()

    asm = line().many()

    return asm
