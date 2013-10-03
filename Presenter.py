class BasePresenter:

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.assignPresenter(self)
        self.model.registerObserver(self)
        self.modelUpdated()

class Presenter(BasePresenter):
    
    def __init__(self, model, view):
        BasePresenter.__init__(self, model, view)
    
    def updateText(self):
        self.model.transferText()

    def modelUpdated(self):
        "presenter model updated"
        self.view.modelUpdated(self.model)
