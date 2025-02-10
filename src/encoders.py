
def direct(opcode_id):
    return opcode_id << 48

#convert string arguments to the right presentation to be included in a instruction
def convert_arguments(argument_token):
    if argument_token.type == 'INT':
        return int(argument_token.value)
    elif argument_token.type == 'FLOAT':
        return int(argument_token.value)

    return 0;

def immediate(opcode_id, argument_token):
    arg = convert_arguments(argument_token)


opcodes = {
    "pushi32": immediate,
    "pushf32": None,
    "addi": None,
    "subi": None,
    "muli": None,
    "divi": None,
    "modi": None,
    "expi": None,
    "addf": None,
    "subf": None,
    "mulf": None,
    "divf": None,
    "modf": None,
    "expf": None,
    "squarei": None,
    "squaref": None,
    "sqrooti": None,
    "sqrootf": None,
    "pop": direct,
}

opcodes_list = list(opcodes.keys())


def encode_opcode(opcode, argument_token=None):
    print(opcode, argument_token.type)

    encoder = opcodes[opcode]
    opcode_offset = opcodes_list.index(opcode) + 1

    if encoder == direct:
        return encoder(opcode_offset)
    elif encoder == immediate:
        arg = convert_arguments(argument_token)
        return encoder(opcode_offset, arg)


if __name__ == "__main__":
    print("pop - {:016X}".format(encode_opcode("pop")))
