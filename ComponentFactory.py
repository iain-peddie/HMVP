from Model import *
from View import *
from Presenter import *
from Mocks import *

class ComponentFactory:

    def __init__(self):
        pass

    def createApplication(self):
        model = BaseModel()
        view = ApplicationView()
        return ApplicationController(model, view, self)

    def createMasterComponent(self, application):    
        view = MasterView()
        presenter = MasterPresenter(MasterModel(), view)
        application.addChild(presenter)
        return presenter

    def createSlaveComponent(self, application):    
        view = SlaveView()
        presenter = SlavePresenter(SlaveModel(), view)
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
        return HierarchicalPresenter(model, view)



