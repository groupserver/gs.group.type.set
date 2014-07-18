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
from __future__ import absolute_import, unicode_literals
from abc import ABCMeta, abstractmethod
from Products.Five.utilities.interfaces import IMarkerInterfaces


class SetABC(object):
    '''Abstract base-class for adaptors that set the type of a group.

:param group: The group that is adapted.
    '''
    __metaclass__ = ABCMeta

    def __init__(self, group):
        self.context = self.group = group

    @abstractmethod
    def set(self):
        '''Set the group type

This method should set the type of the group. This method **must** be
implemented by subclasses.
        '''
        raise NotImplemented('Subclasses must implement ``set()``.')

    @staticmethod
    def add_marker(obj, interfaces):
        '''Add a marker-interfaces to an object

:param object obj: The object to add the marker-interface to.
:param list interfaces: A list of interfaces (as strings) to add to the
                        object.
:returns: ``None``

Group-types are usually implemented as marker interfaces on a group-folder.
This metehod adds the marker interfaces to the object. For example::

        iFaces = ['gs.group.type.closed.interfaces.IGSClosedGroup']
        self.add_marker(self.group, iFaces)

It should be assumed that the previous group-settings have been removed by
an earlier call to :meth:`gs.group.type.set.UnsetABC.unset`.
'''
        adaptedToMarker = IMarkerInterfaces(obj)
        add = adaptedToMarker.dottedToInterfaces(interfaces)
        adaptedToMarker.update(add=add)


class UnsetABC(object):
    '''Abstract base-class for adaptors that unset the type of a group.

:param group: The group that is adapted.

A group *type* can be associated with many different settings. The *unset*
classes remove these settings, so later classes that implment the
:class:`gs.group.type.set.SetABC` abstract base-class can set a new
type with impunity.'''
    __metaclass__ = ABCMeta

    def __init__(self, group):
        self.context = self.group = group

    @abstractmethod
    def unset(self):
        '''Unset the group-type

This method should unset the type of the group. This method **must** be
implemented by subclasses.    '''
        raise NotImplemented('Subclasses must implement ``unset()``.')

    @staticmethod
    def del_marker(obj, interfaces):
        '''Remove a marker-interfaces from an object

:param object obj: The object to remove the marker-interface from.
:param list interfaces: A list of interfaces (as strings) to delete from
                        the object.
:returns: ``None``

Group-types are usually implemented as marker interfaces on a group-folder.
This metehod removes (deltes) the marker interfaces from the object.

For example::

        iFaces = ['gs.group.type.closed.interfaces.IGSClosedGroup']
        self.del_marker(self.group, iFaces)
'''
        adaptedToMarker = IMarkerInterfaces(obj)
        remove = adaptedToMarker.dottedToInterfaces(interfaces)
        adaptedToMarker.update(remove=remove)
