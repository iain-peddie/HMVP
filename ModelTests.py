from WellBehavedPython.TestCase import TestCase
from WellBehavedPython.api import *

from Model import Model

class ModelTests(TestCase):
    
    def __init__(self, name):
        TestCase.__init__(self, name)

    def before(self):
        self.modelUpdatedReceived = False

    def test_model_provides_title(self):
        # Where
        model = Model()

        # When
        title = model.getTitle()

        # Then
        expect(title).toEqual("Exit")

    def test_model_provides_next_text(self):
        # Where
        model = Model()

        # When
        title = model.getNextText()

        # Then
        expect(title).toEqual("I go to the button")

    def test_model_updates_text(self):
        # Where
        model = Model()
        
        # When
        textBefore = model.getCurrentText()[:]
        model.transferText()
        textAfter = model.getCurrentText()

        # Then
        expect(textBefore).toEqual(["Click button to transfer text"])
        expect(textAfter).toEqual(["Click button to transfer text", "I go to the button"])

    def test_model_transfer_triggers_modelChanged(self):
        # Where
        model = Model()
        model.registerObserver(self)

        # When
        model.transferText()

        # Then
        expect(self.modelUpdatedReceived).toBeTrue()

    def test_model_creates_different_next_text_each_time(self):
        # Where
        model = Model()
        
        # When        
        initialNextText = model.getNextText()
        model.transferText()
        firstNextText = model.getNextText()
        model.transferText()
        secondNextText = model.getNextText()

        # Then
        expect(initialNextText).toEqual("I go to the button")
        expect(firstNextText).toEqual("3 items")
        expect(secondNextText).toEqual("4 items")

    def test_can_unregister_observer(self):
        # Where
        model = Model();
        model.registerObserver(self)
        model.unregisterObserver(self)

        # When
        model.transferText()

        # Then
        expect(self.modelUpdatedReceived).toBeFalse()

    def modelUpdated(self):
        self.modelUpdatedReceived = True
