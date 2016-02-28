from tkinter import*
import tkinter.ttk as ttk    #ovveride tkinter widgets
from pyTracert import*


class TraceView(ttk.Frame):

    def __init__(self, master):
        ttk.Frame.__init__(self, master=None)
        self.pack(fill=BOTH, expand=YES)

        self.dest_frame = ttk.Frame(self)
        self.dest_label = ttk.Label(self.dest_frame, text='target', anchor='center', font='Arial 12 bold')
        self.dest_text = ttk.Entry(self.dest_frame)
        self.dest_text.focus_set()
        self.dest_button = ttk.Button(self.dest_frame, text='trace') #command=self.trace
        self.dest_button.bind('<Button-1>', self.trace)
        self.dest_label.pack(side='right', fill=X, expand=YES)
        self.dest_text.pack(side='right', fill=X, expand=YES)
        self.dest_button.pack(side='left', fill=X, expand=YES)
        self.dest_frame.pack(side='top', fill=X, expand=NO)

        self.tree = ttk.Treeview(self, selectmode="extended", columns=('ttl', 'domain_name', 'ip_v4', 'rtt'))
        # hide pseudo column
        self.tree.column('#0', stretch=NO, width=0)
        self.tree.column('ttl', stretch=YES, width=64)
        self.tree.heading('ttl', text='hop(ttl)')
        self.tree.column('domain_name', stretch=YES, width=300)
        self.tree.heading('domain_name', text='domain name')
        self.tree.column('ip_v4', stretch=YES, width=128)
        self.tree.heading('ip_v4', text='IPv4')
        self.tree.column('rtt', stretch=YES, width=256)
        self.tree.heading('rtt', text='RTT')
        self.tree.pack(fill=BOTH, expand=YES)

    def clearView(self):
        for child in self.tree.get_children():
            self.tree.delete(child)

    @staticmethod
    def timeStamp(time):
        return str(round(time*1000, 5))+'ms'

    def trace(self, event):
        self.clearView()
        try:
            if self.dest_text.get() != '':
                tracert = Tracert(self.dest_text.get())
                for i in range(1, tracert.max_hops):
                    ping_res = tracert.ping(i)
                    if ping_res is not None:
                        self.tree.insert('', 'end', values=(ping_res[0], ping_res[1], ping_res[2],
                                                            TraceView.timeStamp(ping_res[3][0]) + ' ' +
                                                            TraceView.timeStamp(ping_res[3][1]) + ' ' +
                                                            TraceView.timeStamp(ping_res[3][2])))
                        self.tree.update()
                        if ping_res[4]:
                            break
        except OSError as e:
            pass





if __name__ == '__main__':
    root = Tk()
    trace_view = TraceView(master=root)
    trace_view.master.title('traceroute')
    trace_view.master.geometry('800x600')
    trace_view.mainloop()

