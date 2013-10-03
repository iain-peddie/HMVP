class Controller:

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.assignController(self)
    
    def updateText(self):
        # TODO : this should extract the text from the view
        #        and provide it to the model for updating...
        self.model.transferText()
