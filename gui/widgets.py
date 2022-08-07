import os
from tkinter import Tk, Frame, TOP, BOTTOM, X, LEFT, RIGHT, Y, BOTH, NORMAL, DISABLED
from tkinter.ttk import Treeview, Scrollbar
from tkinter.scrolledtext import ScrolledText


class MainFrame(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.iconbitmap('gui/images/icon.ico')
        self.title('Python Assembler')
        self.geometry(f"{self.winfo_screenwidth()}x{ self.winfo_screenheight()}")


class Editor(ScrolledText):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(side=TOP, fill=X)


class CMD(ScrolledText):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(side=BOTTOM, fill=X)
        self.config(state=DISABLED)

    def insert(self, *args, **kwargs):
        self.config(state=NORMAL)
        super(CMD, self).insert(*args, **kwargs)
        self.config(state=DISABLED)


class FoldersFrame(Frame):
    nodes: dict = {}

    def __init__(self, *args, **kwargs):
        self.master = args[0]

        super(FoldersFrame, self).__init__(*args, **kwargs)
        self.pack(side=LEFT, fill=Y)

        self.tree = Treeview(self, height=kwargs.get('height', 400))
        self.tree.heading('#0', text='Folders', anchor='w')
        self.tree.pack(side=LEFT, fill=BOTH)

        self.xsb = Scrollbar(self.tree, orient='horizontal', command=self.tree.xview)
        self.xsb.pack(side=BOTTOM, fill=X)
        self.xsb.configure(command=self.tree.xview)

        self.ysb = Scrollbar(self.tree, orient='vertical', command=self.tree.yview)
        self.ysb.pack(side=RIGHT, fill=Y)
        self.ysb.configure(command=self.tree.yview)

        self.tree.configure(yscroll=self.ysb.set, xscroll=self.xsb.set)
        self.tree.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)

        self.abspath = os.path.abspath('')
        self.update_nodes()

    def insert_node(self, parent, text, abspath):
        node = self.tree.insert(parent, 'end', text=text, open=False)
        if os.path.isdir(abspath):
            self.nodes[node] = abspath
            self.tree.insert(node, 'end')

    def open_node(self, event):
        node = self.tree.focus()
        abspath = self.nodes.pop(node, None)
        if abspath:
            self.tree.delete(self.tree.get_children(node))
            for p in os.listdir(abspath):
                self.insert_node(node, p, os.path.join(abspath, p))

    def delete_nodes(self):
        for child in self.tree.get_children():
            self.tree.delete(child)

    def remove_node(self, child):
        self.tree.delete(child)

    def update_nodes(self):
        self.delete_nodes()
        self.insert_node('', self.abspath, self.abspath)
        self.tree.bind('<<TreeviewOpen>>', self.open_node)
