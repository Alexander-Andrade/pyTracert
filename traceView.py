from tkinter import*
import tkinter.ttk as ttk    #ovveride tkinter widgets
from pyTracert import*

class TraceView(Frame):

    def __init__(self, master):
        super.__init__(master)
        self.pack(fill=BOTH, expand=1)
        self.tree = ttk.Treeview(self)
        self.tree.pack(fill=BOTH, expand=YES)
        self.tree.column('ttl', stretch=YES)
        self.tree.heading('ttl', text='hop(ttl)')


if __name__ == '__main__':
    root = Tk()
    trace_view = TraceView(root)
    trace_view.mainloop()

