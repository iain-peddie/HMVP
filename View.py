from tkinter import BOTH, Listbox, END
from tkinter.ttk import Frame, Button, Style, Entry

class View:

    def __init__(self, parent):
        
        self.parent = parent

        self._createWidgets(parent)

    def assignPresenter(self, presenter):
        self.presenter = presenter

    def _createWidgets(self, parent):
        self.top = Frame(parent)

        self.parent.title("Simple")

        self.top.style = Style()
        self.top.style.theme_use("default")
        self.top.grid(sticky="nsew")

        self.updateButton = Button(self.top, text="Update",
                                   command = self.updateButton_clicked)
        self.updateButton.grid(row = 0, column = 0)

        self.transfersList = Listbox(self.top)
        self.transfersList.grid(row = 1, column = 0, sticky = "nsew", columnspan = 2)

        self.updateText = Entry(self.top, text="")
        self.updateText.grid(row = 0, column = 1)

    def modelUpdated(self, model):
        currentText = model.getCurrentText()
        # temporarily, make it just the last item
        self.updateButton["text"] = currentText[-1]
        currentUpdate = self.updateText.get()
        self.updateText.delete(0, len(currentUpdate))
        self.updateText.insert(0, model.getNextText())

        self.transfersList.delete(0, END)
        for line in currentText:
            self.transfersList.insert(END, line)

    def updateButton_clicked(self):
        # This line means we're not in MVC or MVP, but MV:
        self.presenter.updateText()
