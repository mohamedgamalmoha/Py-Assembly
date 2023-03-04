# Py-Assembly
**The package coverts native mips assembly instructions into machine code.**\
It is built based on dataclass using regex and uses pure python functionality, no package is required to be installed.<br>


## How to use it?

### Single Instruction
Use instruction to parse one line of assembly code, in case of being in wrong format an **error** will b thrown.
```python
from py_assembler.instruction import Instruction

add = Instruction('add $s0,$s1,$t1')
# opcode
print(add.op)
# opcode in binary format
print(add.opcode_bin)
# opcode in hex format
print(add.opcode_hex)
# binary representation for whole instruction
print(add.get_bin_repr())
# hex representation for whole instruction
print(add.get_hex_repr())
# instruction sections / parts, eg: iType -> opcode, rs, rt, imm
print(add.get_inst_sections())
# length of instruction sections 
print(add.get_inst_sections_count())
# length of required sections that need to be assigned, it differs based on type
print(add.get_inst_assigned_sections_count())
```
```shell
add
0b0
0x0
00000010000100010100100000100000
0x2114820
('opcode', 'rs', 'rt', 'rd', 'shift', 'func')
6
4
```

### Multiple Instructions
Use parser to parse multi lines of assembly code. The pparser_as_type function returns a lis of parsed 
instructions.
```python
from py_assembler.parse import instructions_parser

instructions = instructions_parser("""
add $t2,$t0,$t1;
or $t2,$t0,$t1;
subi $t2,$t0,#10;
mult $t2,$t0,$s0;
or $t2,$t0,$s4;
ori $t2,$t0,#40;
nor $t2,$t0,$t5;
xor $t2,$t0,$t4;
beq $s3;
div $t2,$t0,$s2;
and $t2,[$t0+10],$s3;
addi $t2,[$t0+$s1],#20;
""")
```

### Filter By Type
It is also possible to filter the instructions based on type
```python
from py_assembler.types import rType, iType, jType

iTypes = list(filter(lambda inst: isinstance(inst.typ, iType), instructions))
rTypes = list(filter(lambda inst: isinstance(inst.typ, rType), instructions))
jTypes = list(filter(lambda inst: isinstance(inst.typ, jType), instructions))
```

### Available Instructions 
Show all supported opcode instructions, others will be added soon.
```python
from py_assembler.types import INSTRUCTIONS

for typ in INSTRUCTIONS:
    print(typ)
```

### Addressing Modes
It is not only register / regular addressing is supported, but also the following
- Immediate 
- Direct
- InDirect
- Base Plus Index
- Relative

 ```python
from py_assembler.regs import RegularReg, ImmediateReg, DirectReg, InDirectReg, BasePlusIndexReg, RelativeReg

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
```
```shell
0b11111
0b1101110
0b1101110
0b10111
0b11110
0b10111
```
In case of being confused of addressing mode, you could use function **get_register_type** which determines the type of addressing in auto way.
In case of non-matching, a None will be returned.
```python
from py_assembler.regs import get_register_type

reg = get_register_type('[ #7 + s7 ]')
# get value of addressing
print(reg.get_val())
# get value of addressing
print(reg.get_bin_repr())
# get value of addressing
print(reg.get_hex_repr())
```
```shell
23
0b10111
0x17
```


## GUI Application 
It is a simple gui application that facilitate the use of this package. 
Instead of dealing with code, it offers a graphical interface. \
You could simply write assembly instructions or upload file, it will translate into binary and hex value.
 ```python
from tkinter import Menu

from gui.menu import file, edit, format, run
from gui.widgets import MainFrame, Editor, CMD


def main():
    root = MainFrame()
    editor = Editor(root, bg='#202020', fg='white')
    cmd = CMD(root, bg='#a5a5a5', fg='yellow', height=400)

    menu_bar = Menu(root)
    file.main(root, editor, menu_bar)
    edit.main(root, editor, menu_bar)
    run.main(root, editor, menu_bar, cmd)
    format.main(root, editor, menu_bar)

    root.mainloop()


if __name__ == "__main__":
    main()
 ```
