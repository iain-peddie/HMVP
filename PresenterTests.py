from WellBehavedPython.TestCase import TestCase
from WellBehavedPython.api import *

from Model import *
from Presenter import *
from View import BaseView
from Mocks import *
from ComponentFactory import MockComponentFactory

import weakref


class MasterPresenterTests(TestCase):
    
    def __init__(self, name):
        TestCase.__init__(self, name)

    def before(self):
        self.model = MasterModel()
        self.view = MockView()
        self.presenter = MasterPresenter(self.model, self.view, self)
        self.createSlaveWindowCalled = False

        # this method makes the test class a mock application controller
    def createSlaveWindow(self):
        self.createSlaveWindowCalled = True

    def test_presenter_catches_model_updated_event_and_presents_to_view(self):
        # Where
        presetner = self.presenter
        model = self.model

        # When
        model.setNextText('something')

        # Then
        expect(self.view.updated).toBeTrue()

    def test_presnter_delegates_cascades_request_to_parent(self):
        # Where
        presenter = self.presenter

        # When
        presenter.requestCreateListener()

        # Then
        expect(self.createSlaveWindowCalled).toBeTrue()

class ApplicationControllerTests(TestCase):
    def __init__(self, name):
        TestCase.__init__(self, name)

    def before(self):
        self.factory = MockComponentFactory()
        self.controller = self.factory.createApplication()
        self.model = self.controller.model
        self.applicationView = self.controller.view

    def test_adding_child_creates_widgets_in_childs_view(self):
        # Where
        controller = self.controller
        childView = MockView()
        child = MasterPresenter(self.model, childView, self)

        # When
        createdBefore = childView.widgetsCreated
        controller.addChild(child)
        createdAfter = childView.widgetsCreated

        # Then
        expect(createdBefore).toBeFalse("widgets should not be created before adding prsenter to parent")
        expect(createdAfter).toBeTrue("widgets should be created after adding presenter to parent")

    def test_calling_show_shows_view(self):
        # When
        shownBefore = self.applicationView.shown
        self.controller.show()
        shownAfter = self.applicationView.shown

        # Then
        expect(shownBefore).toBeFalse("View shouldn't be shown before told to")
        expect(shownAfter).toBeTrue("View shoudl be shown after being told to")

    def test_controller_can_create_master_component(self):
        # Where
        controller = self.controller

        # When
        child = controller.createMasterWindow()

        # Then
        expect(self.factory.lastComponent).toEqual("master")

    def test_controller_can_create_slave_component(self):
        # Where
        controller = self.controller

        # When
        child = controller.createSlaveWindow()

        # Then
        expect(self.factory.lastComponent).toEqual("slave")
        
