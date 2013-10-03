class BaseModel:
    def __init__(self):
        self._observers = []

    def getTitle(self):
        return "Exit"

    def registerObserver(self, observer):
        self._observers.append(observer)

    def unregisterObserver(self, observer):        
        self._observers.remove(observer)

class Model(BaseModel):

    def __init__(self):
        BaseModel.__init__(self)
        self._currentText = ["Click button to transfer text"]
        self._nextText = "I go to the button"

    def _fireModelUpdated(self):
        for observer in self._observers:
            try:
                observer.modelUpdated()
            except Exception as ex:
                print("problem in model updated event")
                print(ex)

    def getCurrentText(self):
        return self._currentText

    def getNextText(self):
        return self._nextText

    def setNextText(self, text):
        self._nextText = text
        self._fireModelUpdated()

    def transferText(self):
        self._currentText.append(self._nextText)
        self._nextText = "{} items".format(len(self._currentText) + 1)
        self._fireModelUpdated()

