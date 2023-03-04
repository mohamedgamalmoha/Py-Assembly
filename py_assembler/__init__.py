"""
Py Assembler Library
----------------------------

It is used to convert native mips assembly instructions into machine code.

:copyright: (c) 2022 Mohamed Gamal Mohamed.
:license: BSD 3-clause. See LICENSE for more details.
"""

from .regs import RegularReg, ImmediateReg, DirectReg, InDirectReg, BasePlusIndexReg, RelativeReg, REGS, get_register_type
from .types import iType, rType, jType, INSTRUCTIONS, get_instruction_type
from .instruction import Instruction
from .parse import instructions_parser


__title__ = 'Py Assembler'
__version__ = '1.0.0'
__author__ = 'Mohamed Gamal Mohamed'
__contact__ = 'moha.gamal@nu.edu.eg'
__myrepo__ = 'https://github.com/mohamedgamalmoha'
__gitrepo__ = ''
__license__ = 'BSD 3-clause'
__copyright__ = 'Copyright 2022'


__all__ = [
    # All-Registers
    REGS,
    # Registers
    RegularReg, ImmediateReg, DirectReg, InDirectReg, BasePlusIndexReg, RelativeReg,
    # Get Register Type
    get_register_type,
    # Types
    iType, rType, jType,
    # All-Instructions
    INSTRUCTIONS,
    # Get Instruction Type By Opcode
    get_instruction_type,
    # Instruction
    Instruction,
    # Parse String
    instructions_parser
]
