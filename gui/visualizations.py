from tkinter import Toplevel, TOP, BOTH
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class Graph(Toplevel):
    def __init__(self, x, y, title, plot_title, x_label, y_label):
        super().__init__()
        self.title(title)

        figure = Figure()
        figure_canvas = FigureCanvasTkAgg(figure, self)
        NavigationToolbar2Tk(figure_canvas, self)

        axes = figure.add_subplot()
        axes.bar(x, y)
        axes.axis('equal')
        axes.set_title(plot_title)
        axes.set_ylabel(y_label)
        axes.set_xlabel(x_label)

        figure_canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
