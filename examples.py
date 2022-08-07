

def gui_example():
    from tkinter import Menu

    from gui.menu import file, edit, format, run
    from gui.widgets import MainFrame, Editor, CMD, FoldersFrame

    root = MainFrame()
    # folders = FoldersFrame(root, bg='red')
    editor = Editor(root, bg='#202020', fg='white')
    cmd = CMD(root, bg='#a5a5a5', fg='yellow', height=400)

    menu_bar = Menu(root)
    file.main(root, editor, menu_bar)
    edit.main(root, editor, menu_bar)
    run.main(root, editor, menu_bar, cmd)
    format.main(root, editor, menu_bar)

    root.mainloop()


    root = MainFrame()
    folders = FoldersFrame(root, bg='red')
    editor = Editor(root, bg='#202020', fg='white')
    cmd = CMD(root, bg='#a5a5a5', fg='yellow', height=400)

    menu_bar = Menu(root)
    file.main(root, editor, menu_bar)
    edit.main(root, editor, menu_bar)
    run.main(root, editor, menu_bar, cmd)
    format.main(root, editor, menu_bar)

    root.mainloop()


def py_assembler_example():
    from py_assembler.parse import parser_as_type
    from py_assembler.types import iType

    instructions = parser_as_type("""add $t2,$t0,$t1;
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
    addi $t2,[$t0+$s1],#20;""")

    itypes = list(filter(lambda inst: isinstance(inst.typ, iType), instructions))
    print(itypes)
    print([i.op for i in instructions])
    for i in instructions:
        print(i)

    bin_repr = [i.get_bin_repr() for i in instructions]
    print(bin_repr)
    print([len(i) for i in bin_repr])


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Test Modules')
    parser.add_argument('--func', type=str,  help='Function name to run')
    args = parser.parse_args()
    name = args.func

    if name is None or name == "py_assembler" or name == "assembler":
        py_assembler_example()
    elif name == "gui":
        gui_example()
    else:
        print("Invalid Parameter, should be assembler or gui")


if __name__ == '__main__':
    main()
