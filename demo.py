#!/usr/bin/env python3

# First attempt at creating a GUI - this follows the TkInter tutorial
# and therfore doesn't make an attempt to use 'proper design'

from tkinter import Tk, BOTH

from WellBehavedPython.api import *
from WellBehavedPython.TestSuite import *
from WellBehavedPython.VerboseConsoleTestRunner import *
from ModelTests import *
from ControllerTests import *

from Controller import *
from Model import *
from View import *

def main():
    root = Tk()
    model = Model()
    root.geometry("250x150+300+300")
    view = View(root, model)
    controller = Controller(model, view)

    root.mainloop()

def unitTest():
    suite = TestSuite()
    suite.add(ModelTests.suite())
    suite.add(ControllerTests.suite())
    runner = VerboseConsoleTestRunner()
    runner.run(suite)
    sys.stdout.flush()

if __name__ == "__main__":
    unitTest()
    main()
