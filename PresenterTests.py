from WellBehavedPython.TestCase import TestCase
from WellBehavedPython.api import *

from Model import Model
from Presenter import Presenter

import weakref

class MockView:

    def __init__(self):
        self.updated = False

    def assignPresenter(self, presneter):
        pass

    def modelUpdated(self, model):
        self.updated = True


class PresenterTests(TestCase):
    
    def __init__(self, name):
        TestCase.__init__(self, name)

    def before(self):
        self.model = Model()
        self.view = MockView()
        self.presenter = Presenter(self.model, self.view)

    def test_setup(self):
        # Where
        presenter = self.presenter
        model = self.model

        # When
        presenter.updateText()

        # Then
        expect(model.getCurrentText()).toEqual(["Click button to transfer text", "I go to the button"])

    def test_presenter_catches_model_updated_event_and_presents_to_view(self):
        # Where
        presetner = self.presenter
        model = self.model

        # When
        model.transferText()

        # Then
        expect(self.view.updated).toBeTrue()
