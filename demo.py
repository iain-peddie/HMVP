#!/usr/bin/env python3

# First attempt at creating a GUI - this follows the TkInter tutorial
# and therfore doesn't make an attempt to use 'proper design'

from tkinter import Tk, BOTH

from WellBehavedPython.api import *
from WellBehavedPython.TestSuite import *
from WellBehavedPython.VerboseConsoleTestRunner import *

from Model import *
from ModelTests import *
from View import *

def main():
    root = Tk()
    model = Model()
    root.geometry("250x150+300+300")
    app = View(root, model)
    root.mainloop()

def unitTest():
    suite = TestSuite()
    suite.add(ModelTests.suite())
    runner = VerboseConsoleTestRunner()
    runner.run(suite)

if __name__ == "__main__":
    unitTest()
    main()
