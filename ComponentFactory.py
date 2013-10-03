from Model import *
from View import *
from Presenter import *
from Mocks import *

class ComponentFactory:

    def __init__(self):
        self.sharedModel = Model()

    def createApplication(self):
        model = BaseModel()
        view = ApplicationView()
        return ApplicationController(model, view, self)

    def createMasterComponent(self, application):    
        view = MasterView()
        presenter = Presenter(self.sharedModel, view)
        application.addChild(presenter)
        return presenter

    def createSlaveComponent(self, application):    
        view = SlaveView()
        presenter = Presenter(self.sharedModel, view)
        application.addChild(presenter)
        return presenter


class MockComponentFactory:
    
    def __init__(self):
        self.lastComponent = ""

    def createApplication(self):
        self.lastComponent = "application"
        model = BaseModel()
        view = MockView()
        return ApplicationController(model, view, self)

    def createMasterWindow(self, parent):
        self.lastComponent = "master"
        return self._createComponent()

    def createSlaveWindow(self, parent):
        self.lastComponent = "slave"
        return self._createComponent()

    def _createComponent(self):
        model = BaseModel()
        view = MockView()
        return BasePresenter(model, view)



