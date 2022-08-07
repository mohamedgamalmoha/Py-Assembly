from py_assembler.instruction import Instruction


def parser_as_type(txt: str) -> list:
    instructions = [i.replace('\n', '').strip() for i in txt.split(';') if i.strip()]
    return list(map(lambda inst: Instruction(inst), instructions))
