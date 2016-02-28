from tkinter import*
import tkinter.ttk as ttk    #ovveride tkinter widgets
from pyTracert import*


class TraceView(ttk.Frame):

    def __init__(self, master):
        ttk.Frame.__init__(self, master=None)
        self.pack(fill=BOTH, expand=YES)
        self.tree = ttk.Treeview(self, selectmode="extended", columns=('ttl', 'domain_name', 'ip_v4', 'rtt'))
        self.tree.pack(fill=BOTH, expand=YES)
        # hide pseudo column
        self.tree.column('#0', stretch=NO, width=0)
        self.tree.column('ttl', stretch=YES)
        self.tree.heading('ttl', text='hop(ttl)')
        self.tree.column('domain_name', stretch=YES)
        self.tree.heading('domain_name', text='domain name')
        self.tree.column('ip_v4', stretch=YES)
        self.tree.heading('ip_v4', text='IPv4')
        self.tree.column('rtt', stretch=YES)
        self.tree.heading('rtt', text='RTT')


if __name__ == '__main__':
    root = Tk()
    trace_view = TraceView(master=root)
    trace_view.master.title('traceroute')
    trace_view.mainloop()

