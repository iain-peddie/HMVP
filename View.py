from tkinter import BOTH
from tkinter.ttk import Frame, Button, Style, Entry


class View(Frame):

    def __init__(self, parent, model):
        Frame.__init__(self, parent)
        self.parent = parent

        # This line puts us into MVC:
        self.model = model
        self.model.registerObserver(self)

        self._createWidgets()

    def _createWidgets(self):
        self.parent.title("Simple")

        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

        self.quitButton = Button(self, text=self.model.getTitle(),
                                 command = self.quit)
        self.quitButton.place(x=10, y=50)
        
        self.updateButton = Button(self, text=self.model.getCurrentText(), 
                                   command = self.updateButton_clicked)
        self.updateButton.place(x=10,y=80)

        self.updateText = Entry(self, text=self.model.getNextText())
        self.updateText.place(x=150, y=80)

        self.modelUpdated(self.model)

    def modelUpdated(self, model):
        self.quitButton["text"] = self.model.getTitle()
        self.updateButton["text"] = self.model.getCurrentText()
        self.updateText.delete(0)
        self.updateText.insert(0, self.model.getNextText())

    def updateButton_clicked(self):
        # This line means we're not in MVC or MVP, but MV:
        self.model.transferText()
