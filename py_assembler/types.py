from typing import Union
from abc import abstractmethod
from dataclasses import dataclass, field

from .regs import Reg, REGISTERS, get_register_type


def bin_conv(num: str, length: int) -> str:
    """Fill bin number with zero till the required length"""
    num = num.replace('0b', '').replace('#', '')
    diff = length - len(num)
    extra = '0' * diff
    return extra + num


def is_parent(cls: type, parent: type) -> bool:
    return parent in cls.__mro__


@dataclass
class Type:
    op: str
    avg_exc_time: int = field(metadata={'': 'ns'})
    opcode: bin = field(metadata={'length': 6})

    reg_pattern: str

    @property
    @abstractmethod
    def values(self) -> tuple:
        """Get instruction parts` name as a tuple"""
        raise NotImplemented

    def get_fields_values(self) -> dict:
        """Get instruction parts as dataclass fields"""
        return {key: value for key, value in self.__dataclass_fields__.items() if key in self.values}

    def get_sub_repr(self) -> tuple:
        """Get instruction parts in bin format as tuple"""
        result = []
        for k, v in self.get_fields_values().items():
            value = getattr(self, k)
            if str(value).strip().replace('#', '').replace('-', '').isnumeric():
                value = bin(value)
            elif is_parent(value.__class__, Reg):
                value = value.get_bin_repr()
            else:
                raise ValueError("Invalid register value")
            result.append(bin_conv(value, v.metadata.get('length')))
        return tuple(result)

    def get_full_repr(self) -> str:
        """Get instruction representation in bin format as str"""
        return ''.join([i.replace('-', '0') for i in self.get_sub_repr()])

    @abstractmethod
    def assign(self, *args) -> None:
        """Assign instruction parts to there values"""
        raise NotImplemented


@dataclass
class iType(Type):

    rs: bin = field(metadata={'length': 5}, init=False)
    rt: bin = field(metadata={'length': 5}, init=False)
    imm: bin = field(metadata={'length': 16}, init=False)

    reg_pattern: str = field(default=r'\$zero,?|\$[a-zA-Z][0-9],?|\$[a-zA-Z]{2},?|\s*#?\d{1,}', init=False)

    @property
    def values(self):
        return 'opcode', 'rs', 'rt', 'imm'
    values.__doc__ = Type.values.__doc__

    def assign(self, rs: str, rt: str, imm: str) -> None:
        self.rs = get_register_type(rs)
        self.rt = get_register_type(rt)
        if str(imm).strip().startswith('#'):
            imm = imm.strip().replace('#', '')
        self.imm = int(imm)
    assign.__doc__ = Type.assign.__doc__


@dataclass
class rType(Type):

    rs: bin = field(metadata={'length': 5}, init=False)
    rt: bin = field(metadata={'length': 5}, init=False)
    rd: bin = field(metadata={'length': 5}, init=False)
    shift: bin = field(default=0b00000, metadata={'length': 5}, init=False)
    func: bin = field(default=0b000000, metadata={'length': 6})

    reg_pattern: str = field(default=r'\$zero,?|\$[a-zA-Z][0-9],?|\$[a-zA-Z]{2},?', init=False)

    @property
    def values(self):
        return 'opcode', 'rs', 'rt', 'rd', 'shift', 'func'
    values.__doc__ = Type.values.__doc__

    @property
    def shamt(self) -> bin:
        """Return shift amount or offset"""
        return self.shift

    def assign(self, rs: str, rt: str, rd: str, shift: bin = None):
        self.rs = get_register_type(rs)
        self.rt = get_register_type(rt)
        self.rd = get_register_type(rd)
        self.shift = shift if shift is not None else self.shift
    assign.__doc__ = Type.assign.__doc__


@dataclass
class jType(Type):
    op: str
    avg_exc_time: float

    opcode: bin = field(metadata={'length': 6})
    pseudo: bin = field(metadata={'length': 26}, init=False)

    reg_pattern: str = field(default=r'\$zero,?|\$[a-zA-Z][0-9],?|\$[a-zA-Z]{2},?', init=False)

    @property
    def values(self):
        return 'opcode', 'pseudo'
    values.__doc__ = Type.values.__doc__

    def assign(self, pseudo):
        if pseudo in REGISTERS:
            pseudo = get_register_type(pseudo)
        elif pseudo.startswith('#'):
            pseudo = pseudo.replace('#', "")
            if not str(pseudo).isnumeric():
                raise ValueError('pseudo should be register or number')
        self.pseudo = pseudo

    assign.__doc__ = Type.assign.__doc__


TYPES = Union[iType, rType, jType]


def get_instruction_type(op: str) -> TYPES:
    """Get instruction type by opcode"""
    return INSTRUCTIONS.get(op.strip())


INSTRUCTIONS = {

    'add':  rType('add', 6, 0b000000, func=0b100000),
    'addi': iType('addi', 6, 0b001000),
    'sub':  rType('sub', 6, 0b000000, func=0b100010),
    'mult': rType('mult', 6,  0b000000, func=0b00011000),
    'div':  rType('div', 6,  0b000000, func=0b011010),

    'and':  rType('and', 6, 0b000000, func=0b100100),
    'andi': iType('andi', 6, 0b1100),
    'or':   rType('or', 6, 0b000000, func=0b100101),
    'ori':  iType('ori', 6, 0b000000),
    'nor':  rType('sub', 6, 0b000000, func=0b100111),
    'xor':  rType('sub', 6, 0b000000, func=0b100110),

    'j': jType('j', 5, 0b000010),
    'beq':  jType('beq', 5, 0b000100),
    'bne':  jType('bne', 5, 0b000101),
    'blez': jType('blez', 5, 0b000110),
    'bqtz': jType('bqtz', 5, 0b000111),

    'sw':   iType('sw', 7, 0b101011),
    'lw':   iType('lw', 8, 0b100011),
    'sb':   iType('sb', 7, 0b101000),
    'lb':   iType('lb', 8, 0b100000),
    'lui':  iType('lui', 8, 0b001111),

    'slt': rType('slt', 6, 0b000000, func=0b101010),
    'slti': iType('slt', 6, 0b001010),
    'sll': rType('slt', 6, 0b000000, func=0b000000),
    'srl': rType('srl', 6, 0b000000, func=0b000010),
    'sra': rType('srl', 6, 0b000000, func=0b000011),
}
