class BasePresenter:

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.assignPresenter(self)
        self.model.registerObserver(self)
        self.modelUpdated()

    def __del__(self):
        self.model.unregisterObserver(self)

    def modelUpdated(self):
        self.view.modelUpdated(self.model)

class HierarchicalPresenter(BasePresenter):

    def __init__(self, model, view):
        BasePresenter.__init__(self, model, view)
        self.parent = None
        self.children = []

    def addChild(self, child):
        child.bindToParent(self)
        self.children.append(child)
        self.view.bindChild(child.view)

    def bindToParent(self, parent):
        self.parent = parent

    def sendUpwardsMessage(self, message, data, bypassSelf = False):
        if not bypassSelf:
            if self.tryToHandleMessage(message, data):
                return
        if self.parent is not None:
            self.parent.sendUpwardsMessage(message, data)

    def sendDownwardsMessage(self, message, data, bypassSelf = False):
        if not bypassSelf:
            if self.tryToHandleMessage(message, data):
                return
        for child in self.children:
            child.sendDownwardsMessage(message, data)

    def tryToHandleMessage(self, message, data):
        return False

class MasterPresenter(HierarchicalPresenter):
    
    def __init__(self, model, view):
        HierarchicalPresenter.__init__(self, model, view)
    
    def updateText(self, updateText):
        self.sendUpwardsMessage("TextUpdated", updateText)
        self.model.resetNextText()

class SlavePresenter(HierarchicalPresenter):
    
    def __init__(self, model, view):
        HierarchicalPresenter.__init__(self, model, view)

    def appendText(self, updateText):
        self.model.appendCurrentText(updateText)

    def tryToHandleMessage(self, message, data):
        handled = False
        if message == "TextUpdated":
            self.appendText(data)
            handled = True
        else:
            # It is important to delegate to base class in
            # else clause. This allows default behavior to
            # be added to the base class
            return HierarchicalPresenter.tryToHandleMessage(self, message, data)
        
        return handled

class ChildCreatorPresenter(HierarchicalPresenter):

    def __init__(self, model, view):
        HierarchicalPresenter.__init__(self, model, view)

    def createMasterWindow(self):
        self.sendUpwardsMessage("CreateMasterWindow", None)

    def createSlaveWindow(self):
        self.sendUpwardsMessage("CreateSlaveWindow", None)

class MasterAndSlavePresenter(HierarchicalPresenter):
    
    def __init__(self, model, view):
        HierarchicalPresenter.__init__(self, model, view)

    def tryToHandleMessage(self, message, data):
        if message == "TextUpdated":
            self.sendDownwardsMessage(message, data, True)
            return True
        return HierarchicalPresenter.tryToHandleMessage(message, data)
    
    
class ApplicationController(HierarchicalPresenter):

    def __init__(self, model, view, factory):
        HierarchicalPresenter.__init__(self, model, view)
        self.factory = factory

    def createMasterWindow(self):
        return self.factory.createMasterComponent(self)

    def createSlaveWindow(self):
        return self.factory.createSlaveComponent(self)

    def createChildCreatorWindow(self):
        return self.factory.createChildCreatorComponent(self)

    def show(self):
        self.view.show()

    def tryToHandleMessage(self, message, data):
        handled = True
        if message == "CreateSlaveWindow":
            self.createSlaveWindow()
        elif message == "CreateMasterWindow":
            self.createMasterWindow()
        else:
            handled = HierarchicalPresenter.tryToHandleMessage(self, message, data)

        if not handled:
            self.sendDownwardsMessage(message, data, True)
        
        return True
        
