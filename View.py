from tkinter import *
from tkinter.ttk import Frame, Button, Style, Entry

class BaseView:

    def __init__(self):
        self.presenter = []
        self.presenterAssigned = False

    def assignPresenter(self, presenter):
        self.presenter = presenter

    def _createWidgets(self, parent):
        """This should be overriden in child views"""
        pass

    def modelUpdated(self, model):
        """This should rerender the view given the
        current state of the model."""
        self.updateFromModel(model)


class HierarchicalView(BaseView):
    def __init__(self):
        BaseView.__init__(self)
        self.bound = False

    def modelUpdated(self, model):
        """This should rerender the view given the
        current state of the model."""
        if self.bound:
            self.updateFromModel(model)

    def tryToBindChild(self, child, componentName):
        # TODO : this probably needs to be able to filter
        #  based on the type and instance of child. The
        # data from this should be injected to the binding process
        # by the presnter
        attachmentPoint = self.getAttachmentPoint(componentName)
        if attachmentPoint is None:
            return False
        child.bindToParent(attachmentPoint)
        return True

    def getAttachmentPoint(self, componentName):
        """This should be overridedn in derived classes if they
        are to contain children. The returned point should be
        a widget that will contain all the widgets in the child's
        view.

        ComponentName is the naem of the type of component. This allows
        filtering based on child types, and certain types of children to
        be attached to certain locations.

        Return
        ------
        This shoudl return the parent widget for the child view, if the
        child should be attached, and None if it should not be attached."""

        return None

    def bindToParent(self, parent):
        if parent is None:
            return
        self._createWidgets(parent)
        self.bound = True
        # push a first update to the view
        self.presenter.modelUpdated()        

            

class ApplicationView(HierarchicalView):
    def __init__(self):
        HierarchicalView.__init__(self)
        self.root = []

    def createWindow(self):
        if self.root == []:
            self._createRoot()
            return self.root
        return Toplevel(self.root)

    def getAttachmentPoint(self, componentNam):
        return self.createWindow()

    def show(self):
        self.root.mainloop()

    def _createRoot(self):
        self.root = Tk()
        self.root.geometry("400x300+300+300")


class MasterView(HierarchicalView):

    def __init__(self):
        HierarchicalView.__init__(self)

    def _createWidgets(self, parent):
        self.top = parent

        self.top.style = Style()
        self.top.style.theme_use("default")
        self.top.grid()

        self.updateButton = Button(self.top, text="Update",
                                   command = self.updateButton_clicked)
        self.updateButton.grid(row = 0, column = 0)

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

class SlaveView(HierarchicalView):
    def __init__(self):
        HierarchicalView.__init__(self)

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
    
class ChildCreatorView(HierarchicalView):

    def __init__(self):
        HierarchicalView.__init__(self)

    def updateFromModel(self, model):
        pass
    
    def _createWidgets(self, parent):
        self.createMasterButton = Button(parent, text = "Create Master", 
                                         command = self.createMasterButton_clicked)
        self.createMasterButton.grid(row = 0, column = 0)

        self.createSlaveButton = Button(parent, text = "Create Slave",
                                        command = self.createSlaveButton_clicked)
        self.createSlaveButton.grid(row = 0, column = 1)

    def createMasterButton_clicked(self):
        self.presenter.createMasterWindow()

    def createSlaveButton_clicked(self):
        self.presenter.createSlaveWindow()

class MasterAndSlaveView(HierarchicalView):
    def __init__(self):
        HierarchicalView.__init__(self)

    def updateFromModel(self, model):
        pass
    
    def _createWidgets(self, parent):
        pass


