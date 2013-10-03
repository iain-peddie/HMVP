class Model:
    def __init__(self):
        self._observers = []
        self._currentText = ["Click button to transfer text"]
        self._nextText = "I go to the button"

    def getTitle(self):
        return "Exit"

    def getCurrentText(self):
        return self._currentText

    def getNextText(self):
        return self._nextText

    def transferText(self):
        self._currentText.append(self._nextText)
        self._fireModelUpdated()

    def registerObserver(self, observer):
        self._observers.append(observer)

    def _fireModelUpdated(self):
        for observer in self._observers:
            try:
                observer.modelUpdated()
            except Exception as ex:
                print("problem in model updated event")
                print(ex)
