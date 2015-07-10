=====================
``gs.group.type.set``
=====================
~~~~~~~~~~~~~~~~~~
Set the group type
~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2014-10-06
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.Net`_.

Introduction
============

This product provides the *Change group type* page_, and the
basic infrastructure for changing the *type* of a group,
including a vocabulary_ that list the different group types.

The group-type alters what the group page looks like, and who can
post to the group [#canpost]_. In addition changing the group
type should also alter some properties on the mailing list. The
default properties are implemented by **deleting** the property
from the mailing list object.

============  ===============  ====================
Type          ``unclosed``     ``replyto``
============  ===============  ====================
Discussion    False (default)   ``group`` (default)
Announcement  False (default)   ``sender``
Support       True              ``sender``
Closed        NA                NA
============  ===============  ====================

:Unclosed: The ``unclosed`` property lingers from ``MailBoxer``,
           and is used to allow non-members to post to a group.


Page
====

The *Change group type* page is provided at ``change-type.html``
in the Group context. It uses the vocabulary_ to list all the
group types, the ``IUnsetType`` interface to figure out the
**current** group-type, and the ``ISetType`` interface to set the
type.

Vocabulary
==========

The vocabulary ``groupserver.GroupType`` lists all the different
group-types that are present on the system.

Resources
=========

- Documentation: see the ``docs`` folder in this product
- Code repository: https://github.com/groupserver/gs.group.type.set
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. [#canpost] See the *Can post* product for more information 
              <https://github.com/groupserver/gs.group.member.canpost>

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
..  _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

..  LocalWords:  canpost unclosed replyto groupserver iopen mpj
