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
    __metaclass__ = ABCMeta

    def __init__(self, group):
        self.context = self.group = group

    @abstractmethod
    def set(self):
        raise NotImplemented('Subclasses must implement ``set()``.')

    @staticmethod
    def add_marker(obj, interfaces):
        adaptedToMarker = IMarkerInterfaces(obj)
        add = adaptedToMarker.dottedToInterfaces(interfaces)
        adaptedToMarker.update(add=add)


class UnsetABC(object):
    __metaclass__ = ABCMeta

    def __init__(self, group):
        self.context = self.group = group

    @abstractmethod
    def unset(self):
        raise NotImplemented('Subclasses must implement ``unset()``.')

    @staticmethod
    def del_marker(obj, interfaces):
        adaptedToMarker = IMarkerInterfaces(obj)
        remove = adaptedToMarker.dottedToInterfaces(interfaces)
        adaptedToMarker.update(remove=remove)
