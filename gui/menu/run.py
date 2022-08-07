from tkinter import Menu, END

from gui.visualizations import Graph
from py_assembler.parse import parser_as_type


def insert_results(txt, cmd):
    instructions = parser_as_type(txt.get(0.0, END))
    cmd.delete("1.0", END)
    for inst in instructions:
        cmd.insert(END, f"\n{inst.inst} // {inst.get_hex_repr()} // {inst.get_bin_repr()}")


def show_results(txt):
    instructions = parser_as_type(txt.get(0.0, END))
    Graph(
        [i.op for i in instructions],
        [i.typ.avg_exc_time for i in instructions],
        "Result",
        "Average Execution Time",
        "Instructions",
        "Time in ns",
    )


def main(root, text, menubar, cmd):
    run_menu = Menu(menubar)
    run_menu.add_command(label="Run", command=lambda: insert_results(text, cmd), accelerator="Ctrl+R")
    run_menu.add_command(label="Graph", command=lambda: show_results(text), accelerator="Ctrl+R")
    root.bind_all("<Control-r>", lambda _: insert_results(text, cmd))
    run_menu.add_separator()
    menubar.add_cascade(label="Debug", menu=run_menu)
    root.config(menu=menubar)
