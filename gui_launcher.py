from tkinter import Menu

from gui.menu import file, edit, format, run
from gui.widgets import MainFrame, Editor, CMD, FoldersFrame


def main():
    root = MainFrame()
    # folders = FoldersFrame(root, bg='red')  # needs to be fixed
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
