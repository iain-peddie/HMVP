class Presenter:

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.assignPresenter(self)
        self.model.registerObserver(self)
        self.modelUpdated(self.model)
    
    def updateText(self):
        # TODO : this should extract the text from the view
        #        and provide it to the model for updating...
        self.model.transferText()

    def modelUpdated(self, model):
        "presenter model updated"
        self.view.modelUpdated(model)
