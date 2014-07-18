# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import unicode_literals
from zope.interface import Interface
from zope.schema import TextLine, Int, Bool, Choice


class IUnsetType(Interface):
    '''The interface for unsetting a group-type.

A group is *adapted* to the :class:`gs.group.type.set.interfaces.IUnsetType`
interface, which is often *implemented* using a class that inherits from
the :class:`gs.group.type.set.UnsetABC` abstract base-class.'''

    #: The name of the group-type. This is a useful way of getting the name
    #: of the **current** group-type::
    #:
    #:    currTypeName = IUnsetType(group).name
    name = TextLine(
        title='Name',
        description='The name of the group type',
        required=True)

    #: The name of the *adaptor* that is used to **set** a group to a type
    #: that *this* class **unsets**. See the documentation for the
    #: :mod:`gs.group.type.set` module for more details.
    setTypeId = TextLine(
        title='Set group-type identifier',
        description='The identifier for the adaptor that sets the '
                    'group-type that this adaptor unsets',
        required=True)

    def unset():
        'Unset the group type'


class ISetType(Interface):
    '''The interface for setting the type of a group.

A group is *adapted* to the :class:`gs.group.type.set.interfaces.ISetType`
interface, which is often *implemented* using a class that inherits from
the :class:`gs.group.type.set.SetABC` abstract base-class.'''

    #: The name of the group-type. It will be displayed in the user
    #: interface.
    name = TextLine(
        title='Name',
        description='The name of the group type',
        required=True)

    #: When the :class:`gs.group.type.set.vocabulary.GroupTypeVocabulary`
    #: vocabulary returns the group-types it orders them by the weight
    #: parameter.
    weight = Int(
        title='Weight',
        description='The sort-order for this group-type',
        default=1024)

    #: True if the group-type should be shown in the user-interface.
    show = Bool(
        title='Show',
        description='True if this group-type should be shown',
        default=True)

    def set():
        'Set the group type'


class IChangeGroupType(Interface):
    groupType = Choice(
        title='Group type',
        description='The type of group',
        vocabulary='groupserver.GroupType',
        required=True)
