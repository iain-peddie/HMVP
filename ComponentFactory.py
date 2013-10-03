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
        presenter = MasterPresenter(self.sharedModel, view, application)
        application.addChild(presenter)
        return presenter

    def createSlaveComponent(self, application):    
        view = SlaveView()
        presenter = BasePresenter(self.sharedModel, view)
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

    def createMasterComponent(self, parent):
        self.lastComponent = "master"
        return self._createComponent()

    def createSlaveComponent(self, parent):
        self.lastComponent = "slave"
        return self._createComponent()

    def _createComponent(self):
        model = BaseModel()
        view = MockView()
        return BasePresenter(model, view)



