========
Adaptors
========

.. currentmodule:: gs.group.type.set

When changing the type of a group two things need to happen: the
old type needs to be unset_, and the new type needs to be
set_. So each of the group types needs to provide two facades,
which are created using adaptors from the Zope Tool Kit.

While most of the the code is simple to the point of being
boiler-plate — because only marker-interfaces need to be cleared
and set on the group — some group-types get more odd. However,
because all the complexity for unsetting and setting group-types
is handled by external classes the core of the `change page`_ is
very simple.

Unset
=====

Before a group-type can be set the old type has to be unset.
Facades (adapters) for clearing the configuration for a given
group-type provide the :class:`interfaces.IUnsetType`
interface. They are registered using ZCML similar to the
following

.. code-block:: xml

   <adapter
    for=".interfaces.IGSDiscussionGroup"
    provides="gs.group.type.set.interfaces.IUnsetType"
    factory=".set.UnsetDiscussionGroup" />

This ZCML snippet registers the code in
:class:`UnsetDiscussionGroup` as an adapter for a
discussion-group (:class:`IGSDiscussionGroup`) to the
:class:`interfaces.IUnsetType` interface.

The code for the facade (adapter) itself is simple, as the
:class:`UnsetABC` abstract base-class can be used to provide most
of the functionality:

.. code-block:: python

  class UnsetDiscussionGroup(UnsetABC):
      name = 'Discussion group'
      setTypeId = 'gs-group-type-discussion-set'

      def unset(self):
          iFaces = ['gs.group.type.discussion.interfaces.IGSDiscussionGroup']
          self.del_marker(self.group, iFaces)

The two attributes, :attr:`name` and :attr:`setTypeId`, are
useful for querying the current state of the group:

.. code-block:: python

  print('This is a {0}'.format(IUnsetType(group).name))

The :attr:`setTypeId` attribute can be thought of as a pointer to
the identifier (*name* in the adapter-parlance of Zope) of the
facade that is used to set_ the group type. It is used by the
`Change page`_ to determine the **current** group type.

Set
===

The facade for setting a group to a particular type provides the
:class:`interfaces.ISetType` interface. The ZCML for registering
such a facade (adapter) is as follows

.. code-block:: xml

  <adapter
    name="gs-group-type-discussion-set"
    for="gs.group.base.interfaces.IGSGroupMarker"
    provides="gs.group.type.set.interfaces.ISetType"
    factory=".set.SetDiscussionGroup"  />

:Note: The adapter for setting a group-type is a *named* adapter,
       because of the ``name`` attribute to the ``<adapter>``
       element. The name **must** be the same as that specified
       in the :attr:`setTypeId` attribute of the corresponding
       unset_ adapter.

The facade itself is simple, as the :class:`SetABC` abstract
base-class is used for providing much of the functionality:

.. code-block:: python

  class SetDiscussionGroup(SetABC):
      name = 'Discussion group'
      weight = 10

      def set(self):
          iFaces = ['gs.group.type.discussion.interfaces.IGSDiscussionGroup']
          self.add_marker(self.group, iFaces)

The :attr:`name` is used to provide a label for the option in the
`Change page`_. The :attr:`weight` attribute is used to order the
adapters in the vocabulary_.

Vocabulary
----------

The *Change* page uses the *vocabulary*
:class:`vocabulary.GroupTypeVocabulary` to list all the facades
that provide the :class:`interfaces.ISetType` interface. While
the vocabulary *can* be instantiated as a stand-alone class,
usually it is used in a ``Choice`` field in a schema, by using
the name of the corresponding ``groupserver.GroupType`` utility:

.. code-block:: python

    groupType = Choice(
        title='Group type',
        description='The type of group',
        vocabulary='groupserver.GroupType',
        required=True)

Change page
===========

Because all the actual functionality for changing a group-type is
farmed off to external classes the core of the Change page is
very simple:

.. code-block:: python

        unsetter = IUnsetType(self.context)
        gsm = getGlobalSiteManager()
        setter = gsm.getAdapter(self.context, ISetType, data['groupType'])

        unsetter.unset()
        setter.set()
