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

    def bindToParent(self, parent):
        self.parent = parent

    def sendUpwardsMessage(self, message, data):
        if self.tryToHandleMessage(message, data):
            return
        if self.parent is not None:
            self.parent.sendUpwardsMessage(message, data)

    def sendDownwardsMessage(self, message, data):
        if self.tryToHandleMessage(message, data):
            return
        for child in self.children:
            child.sendDownwardsMessage(message, data)

    def tryToHandleMessage(self, message, data):
        return False

class MasterPresenter(BasePresenter):
    
    def __init__(self, model, view, application):
        BasePresenter.__init__(self, model, view)
        self.application = application
    
    def updateText(self, updateText):
        self.model.setNextText(updateText)
        # TODO : communcate with parent controller

    def requestCreateListener(self):
        self.application.createSlaveWindow()

class SlavePresenter(BasePresenter):
    
    def __init__(self, model, view, application):
        BasePresenter.__init__(self, model, view)
        self.application = application

    def appendText(self, updateText):
        self.model.appendCurrentText()
    

class ApplicationController(BasePresenter):

    def __init__(self, model, view, factory):
        BasePresenter.__init__(self, model, view)
        self.factory = factory

    def addChild(self, childPresenter):
        viewParent = self.view.createWindow()
        childPresenter.view.bindToParent(viewParent)

    def createMasterWindow(self):
        return self.factory.createMasterComponent(self)

    def createSlaveWindow(self):
        return self.factory.createSlaveComponent(self)

    def show(self):
        self.view.show()


        
        
