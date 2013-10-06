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

    def __init__(self, model, view, parent):
        HierarchicalPresenter.__init__(self, model, view, parent)
