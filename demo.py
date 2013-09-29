#!/usr/bin/env python3

# First attempt at creating a GUI - this follows the TkInter tutorial
# and therfore doesn't make an attempt to use 'proper design'

from tkinter import Tk, BOTH
from tkinter.ttk import Frame, Button, Style, Entry

class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        self._initData()
        self._initUI()

    def _initData(self):
        self._title = "Exit"
        self._text = "Click me"
        self._nextText = "I go to the button"

    def _initUI(self):
        self.parent.title("Simple")

        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

        self.quitButton = Button(self, text=self._title, 
                                 command = self.quit)
        self.quitButton.place(x=10, y=50)
        
        self.updateButton = Button(self, text=self._text, 
                                   command = self.updateButton_clicked)
        self.updateButton.place(x=10,y=80)

        self.updateText = Entry(self, text=self._nextText)
        self.updateText.insert(0, self._nextText)
        self.updateText.place(x=150, y=80)

    def updateButton_clicked(self):
        self.updateButton["text"] = self._nextText

def main():
    root = Tk()
    root.geometry("250x150+300+300")
    app = Example(root)
    root.mainloop()

if __name__ == "__main__":
    main()
