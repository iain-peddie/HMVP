HMVP
====

Backing code for talk summarising heirarchical model-view-presenter/controller patterns

Each demonstration will be in a permament feature branch. The branches as things stand are:

1-all-in-one-class 
------------------

This demonstrates what not to do. It is intented to be used to demonstrate how mixed up all of the concerns are

2-model-view-controller
-----------------------

This demonstrates a more or less standard model-view-controller setup, with the view observing the model, and updating
itself directly from a model referrence. Given that the model and controller can be decoupled from the view, there are
unit tests available in the demonstration.

3-model-view-presenter
----------------------

This modifies the MVC demo in branch #2 to the model-view-presenter setup, with the presenter observing the model, and
then presenting the model to the view to update.

4-shared-model
--------------

This shows how to make two views collaborate by both viewing different parts of a single, shared, model

5-with-application-controller
-----------------------------

This shows how to make two views collaborate via an application controller which is responsible for creating the various
views.
