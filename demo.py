#!/usr/bin/env python3

# First attempt at creating a GUI - this follows the TkInter tutorial
# and therfore doesn't make an attempt to use 'proper design'

from tkinter import Tk, BOTH, END

from WellBehavedPython.api import *
from WellBehavedPython.TestSuite import *
from WellBehavedPython.VerboseConsoleTestRunner import *
from ModelTests import *
from PresenterTests import *

from Presenter import *
from Model import *
from View import *

import sys

def main():
    root = Tk()
    model = Model()
    root.geometry("250x150+300+300")
    view = View(root)
    presenter = Presenter(model, view)

    root.mainloop()

def unitTest():
    suite = TestSuite()
    suite.add(ModelTests.suite())
    suite.add(PresenterTests.suite())
    runner = VerboseConsoleTestRunner()
    results = runner.run(suite)
    if results.countErrors() + results.countFailures() > 0:
        exit(1)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        test = True
        app = True
    else:
        test = False
        app = False
        for argv in sys.argv:
            if argv == "test":
                test = True
            elif argv == "app":
                app = True
            
    if test:
        unitTest()
    
    if app:
        main()
