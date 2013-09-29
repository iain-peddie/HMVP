from WellBehavedPython.TestCase import TestCase
from WellBehavedPython.api import *

from Model import Model

class ControllerTests(TestCase):
    
    def __init__(self, name):
        TestCase.__init__(self, name)

    def setUp(self):
        self.modelUpdatedReceived = False

    def test_setup(self):
        pass
