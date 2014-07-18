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
    'The interface for unsetting a group-type'
    name = TextLine(
        title='Name',
        description='The name of the group type',
        required=True)

    setTypeId = TextLine(
        title='Set group-type identifier',
        description='The identifier for the adaptor that sets the '
                    'group-type that this adaptor unsets',
        required=True)

    def unset():
        'Unset the group type'


class ISetType(Interface):
    'The interface for setting a group-type'
    name = TextLine(
        title='Name',
        description='The name of the group type',
        required=True)

    weight = Int(
        title='Weight',
        description='The sort-order for this group-type',
        default=1024)

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
