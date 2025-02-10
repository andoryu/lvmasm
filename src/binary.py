import encoders

class CodeSection(object):
    labels = {}
    code   = []
    instruction_offset = 0

    def __init__(self):
        pass

    def add_label(self, label):
        self.labels[label] = self.instruction_offset

    def add_instruction(self, instruction):
        self.code.append("instruction")
        self.instruction_offset += 1


class BinaryFormat(object):

    code_sections = []
    current_code_section = None

    def __init__(self):
        pass

    def create_code_section(self):
        section = CodeSection()
        self.code_sections.append(section)
        self.current_code_section = section


def get_label(label_tree_node):
    token = label_tree_node.children[0]
    return token.value.rstrip(":")

def get_opcode(opcode_tree_node):
    token = opcode_tree_node.children[0]
    print(token.value)
    return token.value

def get_argument(argument_tree_node):
    token = argument_tree_node.children[0]
    print(token.value)
    return token.value

def process_instructions(bin, instructions):
    code_section = bin.current_code_section

    for ins in instructions:
        if ins.data != 'instruction':
            return None
        else:
            ins_data = ins.children

            # line with label, opcode and optional argument
            if ins_data[0].data == 'label':
                code_section.add_label(get_label(ins_data[0]))

                if ins_data[1].data == 'opcode':
                    opcode = get_opcode(ins_data[1])
                    argument = None

                    if len(ins_data) == 3 and ins_data[2].data == "argument":
                        encoders.encode_opcode(opcode, ins_data[2].children[0])
                    else:
                        encoders.encode_opcode(opcode)


            # line with label and optional argument
            elif ins_data[0].data == 'opcode':
                opcode = get_opcode(ins_data[0])
                argument = None

                if len(ins_data) == 2 and ins_data[1].data == "argument":
                    encoders.encode_opcode(opcode, ins_data[1].children[0])

                else:
                    encoders.encode_opcode(opcode)

            #code_section.add_instruction('test')


def process_code_sections(bin, sections):

    for section in sections:
        if section.data != "section":
            print("Expected parse tree to have 'section' at this level, instead was '{}'".format(section.data))
            yield None
        else:
            section_type = section.children[0].data
            if section_type == 'code_section':
                bin.create_code_section()

        yield section.children[0].children


def process_program(bin, root):
    if root.data != 'program':
        print("Expected parse tree to start with 'program', instead was '{}'".format(root.data))
        return None
    else:
        return True

def build_binary(lark_tree):
    root = lark_tree
    bin = BinaryFormat()

    if process_program(bin, root):
        for instructions in process_code_sections(bin, root.children):
            if instructions:
                process_instructions(bin, instructions)
