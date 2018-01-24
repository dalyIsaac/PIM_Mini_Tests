from Tkinter import *
import unicodedata

class TestGui(object):

    def __init__(self, master, row=0, indentation_level=0):

        frame = Frame(master)
        frame.grid(row=row, column=0, sticky=W, padx=indentation_level*16)

        self.hi_there = Button(frame, text="Hello", command=self.test_failed)
        self.hi_there.grid(row=0, column=0)

        self.selected = IntVar()
        self.checkbutton = Checkbutton(frame, text="Expand", variable=self.selected)
        self.checkbutton.grid(row=0, column=1)

        self.passfail = Label(frame, text="HAS NOT RUN")
        self.passfail.grid(row=0, column=2)
        
        self.show_more = Button(frame, command=self.show_more_clicked, text="↓")
        self.show_more.grid(row=0, column=3)

        self.output = Text(frame)
        self.output.insert('1.0', 'Hello, world')
        self.output.grid(row=1, column=0, columnspan=5)
        self.output.config(width=50-indentation_level*16)
        self.output.configure(state="disabled")

    def test_passed(self):
        self.passfail['text'] = 'PASSED'
        self.passfail['fg'] = 'dark green'

    def test_failed(self):
        self.passfail['text'] = 'FAILED'
        self.passfail['fg'] = 'red'

    def show_more_clicked(self):
        if self.show_more['text'] == u'\u2193':
            self.show_more['text'] = "↑"
        else:
            self.show_more['text'] = "↓"
            

root = Tk()

gui1 = TestGui(root)
gui2 = TestGui(root, row=1, indentation_level=1)
gui3 = TestGui(root, row=2, indentation_level=2)

root.mainloop()
