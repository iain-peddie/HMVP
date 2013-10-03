from WellBehavedPython.TestCase import TestCase
from WellBehavedPython.api import *

from Model import Model
from Controller import Controller

class MockView:

    def assignController(self, controller):
        self.controller = controller

    def modelUpdated(self, model):
        pass

class ControllerTests(TestCase):
    
    def __init__(self, name):
        TestCase.__init__(self, name)

    def before(self):
        self.model = Model()
        self.view = MockView()
        self.controller = Controller(self.model, self.view)

    def test_setup(self):
        # Where
        controller = self.controller
        model = self.model

        # When
        controller.updateText()

        # Then
        expect(model.getCurrentText()).toEqual("I go to the button")
