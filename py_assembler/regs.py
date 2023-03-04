import re
from abc import abstractmethod
from dataclasses import dataclass, field

REGISTERS = {
    'zero': 0, 'at': 1, 'v0': 2, 'v1': 3,
    'a0': 4, 'a1': 5, 'a2': 6, 'a3': 7,
    't0': 8, 't1': 9, 't2': 10, 't3': 11,
    't4': 12, 't5': 13, 't6': 14, 't7': 15,
    's0': 16, 's1': 17, 's2': 18, 's3': 19,
    's4': 20, 's5': 21, 's6': 22, 's7': 23,
    't8': 24, 't9': 25, 'k0': 26, 'k1': 27,
    'gp': 28, 'sp': 29, 'fp': 30, 'ra': 31
}


def get_register_num(reg_name: str) -> int:
    """Get register number"""
    return REGISTERS.get(reg_name)


@dataclass
class Reg:
    """Base class for mode addressing"""
    string: str
    match_pattern: str = field(init=False)
    parse_pattern: str = field(init=False)

    @classmethod
    def process_str(cls, value: str) -> str:
        """Modify string before it is used in parsing process"""
        return value

    @classmethod
    def match(cls, value: str) -> bool:
        """Validate string is matching the pattern"""
        return bool(re.fullmatch(cls.match_pattern, value))

    def get_proper_str(self) -> str:
        """Get ready string for parsing process"""
        return self.process_str(self.string)

    @property
    def is_matched(self) -> bool:
        """Validate string is matching the pattern"""
        return self.match(self.get_proper_str())

    def parse(self) -> list:
        """Parse string to get it`s parts"""
        # if not self.is_matched:
        #     raise ValueError("Reg does not match")
        return re.findall(self.parse_pattern, self.get_proper_str())

    @abstractmethod
    def get_val(self) -> int:
        """Get value of addressing"""
        raise NotImplemented

    def get_bin_repr(self) -> bin:
        """Get binary value of addressing"""
        return bin(self.get_val())

    def get_hex_repr(self) -> hex:
        """Get hex value of addressing"""
        return hex(self.get_val())

    def __setattr__(self, key, value):
        # deny setting values for match pattern and parse pattern
        if key in ['match_pattern', 'parse_pattern']:
            raise ValueError()
        # remove space from string value
        if key == 'string':
            value = value.strip()
        super().__setattr__(key, value)


@dataclass
class RegularReg(Reg):
    """Regular / Register mode addressing"""
    match_pattern = 'zero|[a-zA-Z]{2}|[a-zA-Z]{1}\d{1}'
    parse_pattern = match_pattern

    def get_val(self) -> int:
        return get_register_num(self.parse()[0])


@dataclass
class ImmediateReg(Reg):
    """Immediate / Constant mode addressing"""
    match_pattern = '#?\d{1,}'
    parse_pattern = '#?(\d{1,})'

    def get_val(self) -> int:
        num = self.parse()[0].replace('-', '')
        if not num.isnumeric():
            raise ValueError
        return int(num)

    get_val.__doc__ = Reg.get_val.__doc__


@dataclass
class DirectReg(ImmediateReg):
    """Direct mode addressing"""
    match_pattern = '\[\s*#?\d{1,}\s*\]'
    parse_pattern = '\[\s*#?(\d{1,})\s*\]'


@dataclass
class InDirectReg(RegularReg):
    """InDirect mode addressing"""
    match_pattern = '\[\s*zero\s*\]|\[\s*[a-zA-Z]{2}\s*\]|\[\s*[a-zA-Z]{1}\d{1}\s*\]'


@dataclass
class BasePlusIndexReg(RegularReg):
    """Base plus index mode addressing"""

    @classmethod
    def process_str(cls, value: str) -> str:
        return value.replace('[', '').replace(']', '')

    process_str.__doc__ = Reg.process_str.__doc__

    @classmethod
    def match(cls, value: str) -> bool:
        s = cls.process_str(value)
        # validating the format of the string
        index = s.find('+')
        if index == -1 or not value.startswith('[') or not value.endswith(']'):
            return False
        # get two registers then match them with pattern
        matched_string = (s[:index].strip(), s[index + 1:].strip())
        return all(map(lambda i: re.fullmatch(cls.match_pattern, i), matched_string))

    match.__doc__ = Reg.match.__doc__

    def get_val(self) -> int:
        s = self.parse()
        if any(i not in REGISTERS for i in s):
            raise ValueError("Invalid register value")
        return sum(get_register_num(i) for i in s)

    get_val.__doc__ = Reg.get_val.__doc__


@dataclass
class RelativeReg(RegularReg):
    """Relative mode addressing"""

    @classmethod
    def process_str(cls, value: str):
        return value.strip().replace('[', '').replace(']', "").replace('#', '')

    process_str.__doc__ = Reg.process_str.__doc__

    @classmethod
    def match(cls, value: str) -> bool:
        s = cls.process_str(value)
        # validating the format of the value
        index = s.find('+')
        if index == -1 or not value.startswith('[') or not value.endswith(']'):
            return False
        # check if one value is numeric and the other is register
        matched_string = (s[:index].strip(), s[index + 1:].strip())
        if matched_string[0].isnumeric():
            matched_string = matched_string[::-1]
        elif not matched_string[0].isnumeric() and not matched_string[1].isnumeric():
            return False
        return bool(re.fullmatch(cls.match_pattern, matched_string[0]))

    match.__doc__ = Reg.match.__doc__

    def get_val(self) -> int:
        return sum(int(i) if i.isnumeric() else get_register_num(i) for i in self.parse())

    get_val.__doc__ = Reg.get_val.__doc__


REGS = RegularReg, ImmediateReg, DirectReg, InDirectReg, BasePlusIndexReg, RelativeReg


def get_register_type(reg_val: str) -> REGS:
    reg_val = reg_val.strip()
    for typ in REGS:
        if typ.match(reg_val):
            return typ(reg_val)


def example() -> None:
    reg = RegularReg('ra')
    print(reg.get_bin_repr())

    reg = ImmediateReg('110')
    print(reg.get_bin_repr())

    reg = DirectReg('[ 110 ]')
    print(reg.get_bin_repr())

    reg = InDirectReg('[ s7 ]')
    print(reg.get_bin_repr())

    reg = BasePlusIndexReg('[ s7 + a3 ]')
    print(reg.get_bin_repr())

    reg = RelativeReg('[ #7 + s7 ]')
    print(reg.get_bin_repr())

    print(get_register_type('[ #7 + s7 ]'))


if __name__ == '__main__':
    example()

# try:
#     t = typ(reg_val)
#     t.get_bin_repr()
#     break
# except:
#     pass
