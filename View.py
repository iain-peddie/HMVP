from tkinter import BOTH
from tkinter.ttk import Frame, Button, Style, Entry


class View:

    def __init__(self, parent, model):
        
        self.parent = parent

        # This line puts us into MVC:
        self.model = model
        self.model.registerObserver(self)

        self._createWidgets(parent)

    def assignController(self, controller):
        self.controller = controller

    def _createWidgets(self, parent):
        self.top = Frame(parent)

        self.parent.title("Simple")

        self.top.style = Style()
        self.top.style.theme_use("default")
        self.top.pack(fill=BOTH, expand=1)

        self.quitButton = Button(self.top, text=self.model.getTitle(),
                                 command = self.top.quit)
        self.quitButton.place(x=10, y=50)
        
        self.updateButton = Button(self.top, text=self.model.getCurrentText(), 
                                   command = self.updateButton_clicked)
        self.updateButton.place(x=10,y=80)

        self.updateText = Entry(self.top, text=self.model.getNextText())
        self.updateText.place(x=150, y=80)

        self.modelUpdated(self.model)

    def modelUpdated(self, model):
        self.quitButton["text"] = self.model.getTitle()
        self.updateButton["text"] = self.model.getCurrentText()
        current = self.updateText.get()
        self.updateText.delete(0, len(current))
        self.updateText.insert(0, self.model.getNextText())

    def updateButton_clicked(self):
        # This line means we're not in MVC or MVP, but MV:
        self.model.transferText()
