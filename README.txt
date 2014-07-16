=====================
``gs.group.type.set``
=====================
~~~~~~~~~~~~~~~~~~
Set the group type
~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2014-17-16
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.Net`_.

Introduction
============

I think what I will do is take a leaf out of the "Can post" code
and use interfaces and adaption to power the selectable group
type. When changing the type of a group two things need to
happen: the old type needs to be unset, and the new type needs to
be set. So I will need two adaptors for each of the group types.

One adaptor will be used to clear out the old settings::

  Change Group Type ──→ IUnset ──→ Unsetter

The adaptor will be fairly simple, adapting a specific group-type
to the IUnset interface, and providing the ``unset()`` method.

The other adaptor provided by each group type will set the new
setting::

  Change Group Type ──→ ISet ──→ Setter

The setters will have to be used to power the vocabulary that is
used with the Change Group Type page. As such each setter will
need the following properties.

* ID: an identifier for the group-type. Used as the token that is
  passed back from the form, and used to get the named adaptor.

* Weight: an integer that is use to order the group types.

* Title: the name of the group type, that is displayed on the
  page.

* Show: a Boolean that allows for particular group-types to be
  turned off.

The setter will provide the ``set()`` method.

Resources
=========

- Code repository: https://source.iopen.net/groupserver/gs.group.type.set
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
..  _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/
