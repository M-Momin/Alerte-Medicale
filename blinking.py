import tkinter as tk

class BlinkingLabel(tk.Label):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.color = 'red'
        self.bgcolor = 'white'
        self.after(500, self.blink)

    def blink(self):
        if self.color == 'white':
            self.color = 'red'
            self.bgcolor = 'white'
        else:
            self.color = 'white'
            self.bgcolor = 'red'
        self.config(fg=self.color, bg=self.bgcolor)
        self.after(1000, self.blink)