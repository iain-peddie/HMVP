from WellBehavedPython.TestCase import TestCase
from WellBehavedPython.api import *

from Model import Model

class ModelTests(TestCase):
    
    def __init__(self, name):
        TestCase.__init__(self, name)

    def setUp(self):
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
        textBefore = model.getCurrentText()
        model.transferText()
        textAfter = model.getCurrentText()

        # Then
        expect(textBefore).toEqual("Click me")
        expect(textAfter).toEqual("I go to the button")

    def test_model_transfer_triggers_modelChanged(self):
        # Where
        model = Model()
        model.registerObserver(self)

        # When
        model.transferText()

        # Then
        expect(self.modelUpdatedReceived).toBeTrue()

    def modelUpdated(self):
        self.modelUpdatedReceived = True
