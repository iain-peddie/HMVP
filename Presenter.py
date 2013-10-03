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



class MasterPresenter(BasePresenter):
    
    def __init__(self, model, view, application):
        BasePresenter.__init__(self, model, view)
        self.application = application
    
    def updateText(self, updateText):
        self.model.setNextText(updateText)
        self.model.transferText()

    def requestCreateListener(self):
        self.application.createSlaveWindow()

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


        
        
