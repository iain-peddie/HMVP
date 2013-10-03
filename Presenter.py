class BasePresenter:

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.assignPresenter(self)
        self.model.registerObserver(self)
        self.modelUpdated()

    def modelUpdated(self):
        self.view.modelUpdated(self.model)

class Presenter(BasePresenter):
    
    def __init__(self, model, view):
        BasePresenter.__init__(self, model, view)
    
    def updateText(self):
        self.model.transferText()

class ApplicationController(BasePresenter):

    def __init__(self, model, view, factory):
        BasePresenter.__init__(self, model, view)
        self.factory = factory

    def addChild(self, childPresenter):
        viewParent = self.view.createWindow()
        childPresenter.view.bindToParent(viewParent)

    def createMasterWindow(self):
        return self.factory.createMasterWindow(self)

    def createSlaveWindow(self):
        return self.factory.createSlaveWindow(self)

    def show(self):
        self.view.show()


        
        
