from WellBehavedPython.TestCase import TestCase
from WellBehavedPython.api import *

from Model import *
from Presenter import *
from View import *
from Mocks import *
from ComponentFactory import MockComponentFactory


class TestingHierarchicalView(HierarchicalView):

    def __init__(self, injectedAttachmentPoint):
        HierarchicalView.__init__(self)
        self.attachmentPoint = injectedAttachmentPoint

    def getAttachmentPoint(self, name):
        return self.attachmentPoint

class HierarhicalPresenterTests(TestCase):

    def __init__(self, name):
        TestCase.__init__(self, name)

    def test_send_unhandled_upwards_message_goes_to_self_and_parent(self):
        # Where
        model = BaseModel()
        view = MockHierarchicalView()
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
        view = MockHierarchicalView()
        parent = MockHierarchicalPresenter(model, view)
        presenter = MockHierarchicalPresenter(model, view, ["TestMessage"])
        parent.addChild(presenter)


        # When
        presenter.sendUpwardsMessage("TestMessage", ["Test data"]);

        # Then
        expect(presenter.recordedMessages).toContain("TestMessage", "Message should be sent to child")
        expect(parent.recordedMessages).Not.toContain("TestMessage", "Message should be sent to parent")

    def test_that_upwards_messages_can_bypass_self_but_not_parent(self):
        # Where
        model = BaseModel()
        view = MockHierarchicalView()
        parent = MockHierarchicalPresenter(model, view)
        presenter = MockHierarchicalPresenter(model, view)
        parent.addChild(presenter)

        # When
        presenter.sendUpwardsMessage("TestMessage", None, bypassSelf = True)

        # Then
        expect(presenter.recordedMessages).Not.toContain("TestMessage", "message should have bypassed child")
        expect(parent.recordedMessages).toContain("TestMessage", "message should have been sent to parent")
        

    def test_that_handled_downwards_message_not_sent_to_children(self):
        # Where
        model = BaseModel()
        view = MockHierarchicalView()
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
        view = MockHierarchicalView()
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
        view = MockHierarchicalView()
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

    def test_that_downwards_messages_can_bypass_self_but_not_children(self):
        # Where
        model = BaseModel()
        view = MockHierarchicalView()
        parent = MockHierarchicalPresenter(model, view)
        child1 =  MockHierarchicalPresenter(model, view)
        child2 = MockHierarchicalPresenter(model, view)
        parent.addChild(child1)
        parent.addChild(child2)

        # When
        parent.sendDownwardsMessage("TestMessage", ["TestData"], bypassSelf = True)
        
        # Then
        expect(parent.recordedMessages).Not.toContain("TestMessage", "Message should bypass parent")
        expect(child1.recordedMessages).toContain("TestMessage", "Message should go to children")
        expect(child2.recordedMessages).toContain("TestMessage", "Message should go to children")

    def test_that_adding_child_binds_child_view_to_parent_view(self):
        # Where
        parentView = MockHierarchicalView()
        childView = MockHierarchicalView()
        parent = MockHierarchicalPresenter(BaseModel(), parentView)
        child = MockHierarchicalPresenter(BaseModel(), childView)

        # When
        contentsBefore = parentView.children[:]
        parent.addChild(child)
        contentsAfter = parentView.children[:]

        # Then
        expect(contentsBefore).Not.toContain(childView)
        expect(contentsAfter).toContain(childView)        

    def test_that_adding_child_to_HierarchicalView_sends_attachment_point_to_child_view(self):
        # Where
        mockAttachmentPoint = "ChildAttachmentPoint"
        parentView = TestingHierarchicalView(mockAttachmentPoint)
        childView = MockHierarchicalView()
        parent = MockHierarchicalPresenter(BaseModel(), parentView)
        child = MockHierarchicalPresenter(BaseModel(), childView)

        # When
        parent.addChild(child)

        # Then
        expect(childView.bound).toBeTrue("Child should have been bound to parent")
        expect(childView.parent).toEqual(mockAttachmentPoint)

    def test_that_component_not_added_if_view_not_added(self):
        # Where
        mockAttachmentPoint = "ChildAttachmentPoint"
        parentView = MockHierarchicalView("Mock")
        childView = MockHierarchicalView()
        parent = MockHierarchicalPresenter(BaseModel(), parentView)
        child = MockHierarchicalPresenter(BaseModel(), childView)

        # When
        parent.addChild(child)

        # Then
        expect(childView.bound).toBeFalse("Child should have been bound to parent")
        expect(parent.children).Not.toContain(child)
    

class MasterPresenterTests(TestCase):
    
    def __init__(self, name):
        TestCase.__init__(self, name)

    def before(self):
        self.model = MasterModel()
        self.view = MockHierarchicalView()
        self.presenter = MasterPresenter(self.model, self.view)
        self.parent = MockHierarchicalPresenter(self.model, self.view)
        self.parent.addChild(self.presenter)

    def test_presenter_catches_model_updated_event_and_presents_to_view(self):
        # Where
        presetner = self.presenter
        model = self.model

        # When
        model.setNextText('something')

        # Then
        expect(self.view.updated).toBeTrue()

    def test_presenter_updateText_sends_TextUpdated_message(self):
        # Where
        presenter = self.presenter
        sentText = "I am the sent text"
        
        # When
        presenter.updateText(sentText)

        # Then
        expect(self.parent.recordedMessages).toContain("TextUpdated")
        expect(self.parent.recordedData).toContain(sentText)
        expect(self.model.getNextText()).toEqual("3 items")


class SlavePresenterTests(TestCase):

    def __init__(self, name):
        TestCase.__init__(self, name)

    def test_that_TextUpdated_meessage_handled_by_appending_text_to_model(self):
        # Where
        model = SlaveModel()
        view = MockView()
        presenter = SlavePresenter(model, view)

        # When
        presenter.tryToHandleMessage("TextUpdated", "UpdatedText")
        
        # Then
        expect(model.getCurrentText()).toContain("UpdatedText")

class ChildCreatorPresenterTests(TestCase):
    def __init__(self, name):
        TestCase.__init__(self, name)

    def before(self):
        self.presenter = ChildCreatorPresenter(BaseModel(), MockView())
        self.parent = MockHierarchicalPresenter(BaseModel(), MockHierarchicalView())
        self.parent.addChild(self.presenter)

    def test_that_presenter_createMasterWindow_sends_message_to_parent(self):
        # Where
        presenter = self.presenter

        # When
        presenter.createMasterWindow()

        # Then
        expect(self.parent.recordedMessages).toContain("CreateMasterWindow")

    def test_that_presenter_createSlaveWindow_sends_message_to_parent(self):
        # Where
        presenter = self.presenter

        # When
        presenter.createSlaveWindow()

        # Then
        expect(self.parent.recordedMessages).toContain("CreateSlaveWindow")

    def test_that_presenter_createMasterAndSlaveWindow_sends_message_to_parent(self):
        # Where
        presenter = self.presenter

        # When
        presenter.createMasterAndSlaveWindow()

        # Then
        expect(self.parent.recordedMessages).toContain("CreateMasterAndSlaveWindow")


    def test_that_presenter_createSlaveAndMasterWindow_sends_message_to_parent(self):
        # Where
        presenter = self.presenter

        # When
        presenter.createSlaveAndMasterWindow()

        # Then
        expect(self.parent.recordedMessages).toContain("CreateSlaveAndMasterWindow")


class MasterAndSlavePresenterTests(TestCase):
    def __init__(self, name):
        TestCase.__init__(self, name)

    def before(self):
        self.parent = MockHierarchicalPresenter(BaseModel(), MockHierarchicalView())
        self.presenter = MasterAndSlavePresenter(BaseModel(), MockHierarchicalView())
        self.child1 = MockHierarchicalPresenter(BaseModel(), MockView())
        self.child2 = MockHierarchicalPresenter(BaseModel(), MockView())

        self.parent.addChild(self.presenter)
        self.presenter.addChild(self.child1)
        self.presenter.addChild(self.child2)

    def test_that_presenter_bounces_TextUpdated_message_back_to_children(self):
        # Where
        sourceChild = self.child1
        targetChild = self.child2
        presenter = self.presenter
        parent = self.parent

        # When
        sourceChild.sendUpwardsMessage("TextUpdated", "boo", bypassSelf = True)

        # Then
        expect(parent.recordedMessages).Not.toContain("TextUpdated")
        expect(sourceChild.recordedMessages).toContain("TextUpdated")
        expect(targetChild.recordedMessages).toContain("TextUpdated")
        

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
        controller.view = TestingHierarchicalView("MockAttachmentPoint")
        childView = MockHierarchicalView()
        child = MasterPresenter(self.model, childView)

        # When
        createdBefore = childView.widgetsCreated
        controller.addChild(child)
        createdAfter = childView.widgetsCreated

        # Then
        expect(createdBefore).toBeFalse("widgets should not be created before adding presenter to parent")
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
        controller.tryToHandleMessage("CreateSlaveWindow", None)

        # Then
        expect(self.factory.lastComponent).toEqual("slave")
        expect(len(self.controller.children)).toEqual(1)

    def test_that_controller_can_create_master_component(self):
        # Where
        controller = self.controller

        # When
        controller.tryToHandleMessage("CreateMasterWindow", None)

        # Then
        expect(self.factory.lastComponent).toEqual("master")
        expect(len(self.controller.children)).toEqual(1)        

    def test_that_application_can_create_child_creator_component(self):
        # Where
        controller = self.controller

        # When
        controller.createChildCreatorWindow()

        # Then
        expect(self.factory.lastComponent).toEqual("child creator")
        expect(len(self.controller.children)).toEqual(1)        

    def test_that_application_can_create_master_and_child_component(self):
        # Where
        controller = self.controller

        # When
        controller.tryToHandleMessage("CreateMasterAndSlaveWindow", None)

        # Then
        expect(self.factory.lastComponent).toEqual("master and slave")
        expect(len(self.controller.children)).toEqual(1)

    def test_that_application_can_create_child_and_master_component(self):
        # Where
        controller = self.controller

        # When
        controller.tryToHandleMessage("CreateSlaveAndMasterWindow", None)

        # Then
        expect(self.factory.lastComponent).toEqual("slave and master")
        expect(len(self.controller.children)).toEqual(1)


    def test_that_unexpected_messages_are_sent_downwards(self):
        # Where
        controller = self.controller
        child = self.factory.createSlaveComponent(controller)

        # When
        controller.tryToHandleMessage("Unexpected" , "")
        
        # Then
        expect(child.recordedMessages).toContain("Unexpected")
        

        
