========================
:mod:`gs.group.type.set`
========================
:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 23015-07-10
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.Net`_.

..  _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

The *Change group type* page needs to be able to switch *from*
any group type *to* any group type. However, it should remain
ignorant of the implementation details of all the group
types. This product provides the architecture to allow the
classes that provide the different group types to register with
the *Change group type* page, and it allows the page to switch to
an arbitrary group type.  Contents:

.. toctree::
   :maxdepth: 2

   adaptors
   api
   HISTORY


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Resources
=========

- Code repository: https://github.com/groupserver/gs.group.type.set
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
