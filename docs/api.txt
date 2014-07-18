``gs.group.type.set`` API
=========================

The application programming-interface for this product is
provided by three components: the `abstract base classes`_, the
interfaces_ and the vocabulary_.

Abstract base classes
---------------------

There are two abstract base classes, :class:`SetABC` and
:class:`UnsetABC`, that are used to provide the core
functionality of the Set and Unset classes.

.. autoclass:: gs.group.type.set.SetABC
   :members:

.. autoclass:: gs.group.type.set.UnsetABC
   :members:

Interfaces
----------

There are two interfaces, :class:`ISetType` and
:class:`IUnsetType`, that are used to adapt the set and unset
classes.

.. autoclass:: gs.group.type.set.interfaces.ISetType
   :members:

.. autoclass:: gs.group.type.set.interfaces.IUnsetType
   :members:

Vocabulary
----------

The :class:`GroupTypeVocabulary` vocabulary is used to list all
the classes that adapt a group to the :class:`ISetType`
interface.

.. autoclass:: gs.group.type.set.vocabulary.GroupTypeVocabulary
   :members: __iter__, __len__, __contains__, adaptors, adaptorIds
