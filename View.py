from tkinter import *
from tkinter.ttk import Frame, Button, Style, Entry

class BaseView:

    def __init__(self):
        self.bound = False
        self.presenter = []
        self.presenterAssigned = False

    def assignPresenter(self, presenter):
        self.presenter = presenter

    def bindToParent(self, parent):
        self._createWidgets(parent)
        self.bound = True
        # push a first update to the view
        self.presenter.modelUpdated()
        

    def _createWidgets(self, parent):
        """This should be overriden in child views"""
        pass

    def modelUpdated(self, model):
        """This should rerender the view given the
        current state of the model."""
        if self.bound:
            self.updateFromModel(model)
            

class ApplicationView(BaseView):
    def __init__(self):
        BaseView.__init__(self)
        self.root = []

    def createWindow(self):
        if self.root == []:
            self._createRoot()
            return self.root
        return Toplevel(self.root)

    def show(self):
        self.root.mainloop()

    def _createRoot(self):
        self.root = Tk()
        self.root.geometry("400x300+300+300")


class MasterView(BaseView):

    def __init__(self):
        BaseView.__init__(self)

    def _createWidgets(self, parent):
        self.top = parent

        self.top.style = Style()
        self.top.style.theme_use("default")
        self.top.grid()

        self.updateButton = Button(self.top, text="Update",
                                   command = self.updateButton_clicked)
        self.updateButton.grid(row = 0, column = 0)

        self.createListenerButton = Button(self.top, text="Create Listener", 
                                        command = self.createListenerButton_clicked)
        self.createListenerButton.grid(row = 1, column = 0)

        self.updateText = Entry(self.top, text="")
        self.updateText.grid(row = 0, column = 1)

    def updateFromModel(self, model):
        
        # temporarily, make it just the last item
        currentUpdate = self.updateText.get()
        self.updateText.delete(0, len(currentUpdate))
        self.updateText.insert(0, model.getNextText())

    def updateButton_clicked(self):
        # This line means we're not in MVC or MVP, but MV:
        currentUpdate = self.updateText.get()
        self.presenter.updateText(currentUpdate)

    def createListenerButton_clicked(self):
        self.presenter.requestCreateListener()

class SlaveView(BaseView):
    def __init__(self):
        BaseView.__init__(self)

    def _createWidgets(self, parent):
        self.top = parent

        self.top.style = Style()
        self.top.style.theme_use("default")
        self.top.grid()

        self.transfersList = Listbox(self.top)
        self.transfersList.grid(row = 1, column = 0, sticky = "nsew", columnspan = 2)

    def updateFromModel(self, model):
        currentText = model.getCurrentText()
        # temporarily, make it just the last item

        self.transfersList.delete(0, END)
        for line in currentText:
            self.transfersList.insert(END, line)

    def updateButton_clicked(self):    
        self.presenter.updateText()
    
