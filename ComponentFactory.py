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

    def createMasterComponent(self, parent):    
        view = MasterView()
        presenter = MasterPresenter(MasterModel(), view)
        parent.addChild(presenter)
        return presenter

    def createSlaveComponent(self, parent):    
        view = SlaveView()
        presenter = SlavePresenter(SlaveModel(), view)
        parent.addChild(presenter)
        return presenter

    def createChildCreatorComponent(self, parent):
        view = ChildCreatorView()
        presenter = ChildCreatorPresenter(BaseModel(), view)
        parent.addChild(presenter)
        return presenter


class MockComponentFactory:
    
    def __init__(self):
        self.lastComponent = ""

    def createApplication(self):
        self.lastComponent = "application"
        model = BaseModel()
        view = MockHierarchicalView()
        return ApplicationController(model, view, self)

    def createMasterComponent(self, parent):
        self.lastComponent = "master"
        return self._createComponent(parent)

    def createSlaveComponent(self, parent):
        self.lastComponent = "slave"
        return self._createComponent(parent)

    def createChildCreatorComponent(self, parent):
        self.lastComponent = "child creator"
        return self._createComponent(parent)

    def _createComponent(self, parent):
        model = BaseModel()
        view = MockHierarchicalView()
        component = MockHierarchicalPresenter(model, view)
        parent.addChild(component)
        return component
        



