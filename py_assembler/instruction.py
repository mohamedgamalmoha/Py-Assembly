import re
from dataclasses import dataclass

from .types import iType, TYPES, get_instruction_type


OP_CODE_PATTERN = r'^[a-zA-Z]{1,4}\s+'


@dataclass
class Instruction:
    """MIPS Assembly Instruction"""

    inst: str
    typ: TYPES = None

    def __post_init__(self) -> None:
        """Set instruction type after class initialization"""
        op = self.parse(self.inst, OP_CODE_PATTERN).strip()

        if op == 'subi':
            # in case of op code in subi, change op to addi and then get the second complement of number
            op = 'addi'
            number_regex = r',\s*#?\s*(\d+)'
            number = str(1 - int(re.findall(number_regex, self.inst)[0]))  # second complement
            self.inst = re.sub(number_regex, f", {number}", self.inst)

        typ = get_instruction_type(op)
        if not typ:
            raise ValueError("Invalid instruction code")

        self.typ = typ

        inst = self.inst[len(op)+1:]  # get instruction without op part
        rest = inst.replace('$', '').strip().split(',')  # instructions parts - registers & immediate - as list.

        if isinstance(self.typ, iType) and len(rest) == 2:
            rest.insert(1, 'zero')
        self.typ.assign(*rest)

    @staticmethod
    def parse(s: str, pattern: str) -> str:
        """Parse string s with required pattern"""
        m = re.compile(pattern).search(s)
        return m.group(0)

    @property
    def opcode_hex(self) -> hex:
        """Return instruction code in hex format"""
        return hex(self.typ.opcode)

    @property
    def opcode_bin(self) -> hex:
        """Return instruction code in binary format"""
        return bin(self.typ.opcode)

    @property
    def op(self) -> str:
        """Get opcode name"""
        return self.typ.op

    def get_bin_repr(self) -> bin:
        """Gwt binary representation for whole instruction"""
        return self.typ.get_full_repr()

    def get_hex_repr(self) -> hex:
        """Gwt hex representation for whole instruction"""
        return hex(int(self.get_bin_repr(), 2))

    def get_inst_sections(self) -> tuple:
        """Return instructions sections / parts"""
        return self.typ.values

    def get_inst_sections_count(self) -> int:
        """"Return length of instructions sections / parts"""
        return self.typ.assign.length


def example():
    add = Instruction('add $s0,$s1,$t1')
    print(add.get_bin_repr())
    print(add.get_hex_repr(), '\n')

    addi = Instruction('addi $s0, $s1, #45')
    print(addi.get_bin_repr())
    print(addi.get_hex_repr(), '\n')

    _or = Instruction('or $t2,$t0,$t1')
    print(_or.get_bin_repr())
    print(_or.get_hex_repr(), '\n')

    subi = Instruction('subi $t3, $t0, # 10')
    print(subi.get_bin_repr())
    print(subi.get_hex_repr(), '\n')

    lw = Instruction('lw $t0, #50')
    print(lw.get_bin_repr())
    print(lw.get_hex_repr(), '\n')

    beq = Instruction('beq $t0')
    print(beq.get_bin_repr())
    print(beq.get_hex_repr(), '\n')


if __name__ == '__main__':
    example()
