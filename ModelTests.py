from WellBehavedPython.TestCase import TestCase
from WellBehavedPython.api import *

from Model import Model

class ModelTests(TestCase):
    
    def __init__(self, name):
        TestCase.__init__(self, name)

    def test_model_provides_title(self):
        # Where
        model = Model()

        # When
        title = model.getTitle()

        # Then
        expect(title).toEqual("Exit")

