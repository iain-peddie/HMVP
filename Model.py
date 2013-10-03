class BaseModel:
    def __init__(self):
        self._observers = []

    def getTitle(self):
        return "Exit"

    def registerObserver(self, observer):
        self._observers.append(observer)

    def unregisterObserver(self, observer):        
        self._observers.remove(observer)

    def _fireModelUpdated(self):
        for observer in self._observers:
            try:
                observer.modelUpdated()
            except Exception as ex:
                print("problem in model updated event")
                print(ex)

class MasterModel(BaseModel):

    def __init__(self):
        BaseModel.__init__(self)
        self._nextText = "I go to the button"
        self.numberOfEntries = 1

    def getNextText(self):
        return self._nextText

    def setNextText(self, text):
        self._nextText = text
        self._fireModelUpdated()
    
    def resetNextText(self):
        self.numberOfEntries = self.numberOfEntries + 1
        self._nextText = "{} items".format(self.numberOfEntries + 1)
        self._fireModelUpdated()

class SlaveModel(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)
        self._currentText = ["Click button to transfer text"]

    def getCurrentText(self):
        return self._currentText

    def appendCurrentText(self, newText):
        self._currentText.append(newText)
        self._fireModelUpdated()

