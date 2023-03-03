"""
Py Assembler Library
----------------------------

It is used to convert native mips assembly instructions into machine code.

:copyright: (c) 2022 Mohamed Gamal Mohamed.
:license: BSD 3-clause. See LICENSE for more details.
"""

from .regs import RegularReg, ImmediateReg, DirectReg, InDirectReg, BasePlusIndexReg, RelativeReg
from .types import iType, rType, jType, INSTRUCTIONS
from .instruction import Instruction
from .parse import parser_as_type


__title__ = 'Py Assembler'
__version__ = '1.0.0'
__author__ = 'Mohamed Gamal Mohamed'
__contact__ = 'moha.gamal@nu.edu.eg'
__myrepo__ = 'https://github.com/mohamedgamalmoha'
__gitrepo__ = ''
__license__ = 'BSD 3-clause'
__copyright__ = 'Copyright 2022'


__all__ = [
    # Registers
    RegularReg, ImmediateReg, DirectReg, InDirectReg, BasePlusIndexReg, RelativeReg,
    # Types
    iType, rType, jType,
    # All-Instructions
    INSTRUCTIONS,
    # Instruction
    Instruction,
    # Parse String
    parser_as_type
]
