from View import BaseView
from Presenter import HierarchicalPresenter

class MockView(BaseView):

    def __init__(self):
        self.updated = False
        self.widgetsCreated = False
        self.shown = False

    def assignPresenter(self, presenter):
        self.presenter = presenter

    def modelUpdated(self, model):
        self.updated = True

    def _createWidgets(self, parent):
        self.widgetsCreated = True

    def createWindow(self):
        return self

    def show(self):
        self.shown = True

class MockHierarchicalView(MockView):
    def __init__(self):
        self.updated = False
        self.widgetsCreated = False
        self.shown = False
        self.children = []
        self.bound = False

    def bindChild(self, child):
        self.children.append(child)

    def bindToParent(self, parent):
        self.bound = True
        self.parent = parent


class MockHierarchicalPresenter(HierarchicalPresenter):

    def __init__(self, model, view, handledMessages = []):
        HierarchicalPresenter.__init__(self, model, view)
        self.handledMessages = handledMessages
        self.recordedMessages = []
        self.recordedData = []

    def tryToHandleMessage(self, message, data):
        self.recordedMessages.append(message)
        self.recordedData.append(data)
        return message in self.handledMessages
    
