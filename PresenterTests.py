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

    def test_send_unhandled_upwards_message_goes_to_self_and_parent(self):
        # Where
        model = BaseModel()
        view = BaseView()
        parent = MockHierarchicalPresenter(model, view)
        presenter = MockHierarchicalPresenter(model, view)
        parent.addChild(presenter)


        # When
        presenter.sendUpwardsMessage("TestMessage", ["Test data"]);
        expect(presenter.recordedMessages).toContain("TestMessage", "Message should be sent to child")
        expect(parent.recordedMessages).toContain("TestMessage", "Message should be sent to parent")

    def test_that_handled_upwards_message_dont_go_to_parent(self):
        # Where
        model = BaseModel()
        view = BaseView()
        parent = MockHierarchicalPresenter(model, view)
        presenter = MockHierarchicalPresenter(model, view, ["TestMessage"])
        parent.addChild(presenter)


        # When
        presenter.sendUpwardsMessage("TestMessage", ["Test data"]);

        # Then
        expect(presenter.recordedMessages).toContain("TestMessage", "Message should be sent to child")
        expect(parent.recordedMessages).Not.toContain("TestMessage", "Message should be sent to parent")

    def test_that_handled_downwards_message_not_sent_to_children(self):
        # Where
        model = BaseModel()
        view = BaseView()
        parent = MockHierarchicalPresenter(model, view, ["TestMessage"])
        child1 =  MockHierarchicalPresenter(model, view)
        child2 = MockHierarchicalPresenter(model, view)
        parent.addChild(child1)
        parent.addChild(child2)

        # When
        parent.sendDownwardsMessage("TestMessage", ["TestData"])
        
        # Then
        expect(parent.recordedMessages).toContain("TestMessage", "Message should be sent to parent")
        expect(child1.recordedMessages).Not.toContain("TestMessage", "Message should not go to children")
        expect(child2.recordedMessages).Not.toContain("TestMessage", "Message should not go to children")

    def test_that_unhandled_downwards_message_sent_to_all_children(self):
        # Where
        model = BaseModel()
        view = BaseView()
        parent = MockHierarchicalPresenter(model, view)
        child1 =  MockHierarchicalPresenter(model, view)
        child2 = MockHierarchicalPresenter(model, view)
        parent.addChild(child1)
        parent.addChild(child2)

        # When
        parent.sendDownwardsMessage("TestMessage", ["TestData"])
        
        # Then
        expect(parent.recordedMessages).toContain("TestMessage", "Message should be sent to parent")
        expect(child1.recordedMessages).toContain("TestMessage", "Message should go to children")
        expect(child2.recordedMessages).toContain("TestMessage", "Message should go to children")

    def test_that_downwward_message_being_handled_does_not_block_message_to_siblings(self):
        # Where
        model = BaseModel()
        view = BaseView()
        parent = MockHierarchicalPresenter(model, view)
        child1 =  MockHierarchicalPresenter(model, view, ["TestMessage"])
        child2 = MockHierarchicalPresenter(model, view)
        parent.addChild(child1)
        parent.addChild(child2)

        # When
        parent.sendDownwardsMessage("TestMessage", ["TestData"])
        
        # Then
        expect(parent.recordedMessages).toContain("TestMessage", "Message should be sent to parent")
        expect(child1.recordedMessages).toContain("TestMessage", "Message should go to children")
        expect(child2.recordedMessages).toContain("TestMessage", "Message should go to children")        

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
        
