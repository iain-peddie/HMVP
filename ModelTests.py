from WellBehavedPython.TestCase import TestCase
from WellBehavedPython.api import *

from Model import *

class MasterModelTests(TestCase):
    
    def __init__(self, name):
        TestCase.__init__(self, name)

    def before(self):
        self.modelUpdatedReceived = False

    def test_model_provides_title(self):
        # Where
        model = MasterModel()

        # When
        title = model.getTitle()

        # Then
        expect(title).toEqual("Exit")

    def test_model_provides_next_text(self):
        # Where
        model = MasterModel()

        # When
        title = model.getNextText()

        # Then
        expect(title).toEqual("I go to the button")

    def test_model_updates_text(self):
        # Where
        model = SlaveModel()
        
        # When
        textBefore = model.getCurrentText()[:]
        model.appendCurrentText('I go to the button')
        textAfter = model.getCurrentText()

        # Then
        expect(textBefore).toEqual(["Click button to transfer text"])
        expect(textAfter).toEqual(["Click button to transfer text", "I go to the button"])

    def test_model_transfer_triggers_modelChanged(self):
        # Where
        model = SlaveModel()
        model.registerObserver(self)

        # When
        model.appendCurrentText("something")

        # Then
        expect(self.modelUpdatedReceived).toBeTrue()

    def test_model_creates_different_next_text_each_time(self):
        # Where
        model = MasterModel()
        
        # When        
        initialNextText = model.getNextText()
        model.resetNextText()
        firstNextText = model.getNextText()
        model.resetNextText()
        secondNextText = model.getNextText()

        # Then
        expect(initialNextText).toEqual("I go to the button")
        expect(firstNextText).toEqual("3 items")
        expect(secondNextText).toEqual("4 items")

    def test_can_unregister_observer(self):
        # Where
        model = MasterModel();
        model.registerObserver(self)
        model.unregisterObserver(self)

        # When
        model.setNextText("")

        # Then
        expect(self.modelUpdatedReceived).toBeFalse()

    def modelUpdated(self):
        self.modelUpdatedReceived = True
