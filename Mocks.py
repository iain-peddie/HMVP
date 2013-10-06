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

class MockHierarchicalPresenter(HierarchicalPresenter):

    def __init__(self, model, view, handledMessages = []):
        HierarchicalPresenter.__init__(self, model, view)
        self.handledMessages = handledMessages
        self.recordedMessages = []

    def tryToHandleMessage(self, message, data):
        self.recordedMessages.append(message)
        return message in self.handledMessages
    
