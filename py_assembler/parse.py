from typing import List
from py_assembler.instruction import Instruction


def instructions_parser(instructions_str: str) -> List[Instruction]:
    """Parse multiple instructions at once from string"""
    return [
        Instruction(i.replace('\n', '').strip())
        for i in instructions_str.split(';')
        if i.strip()
    ]
