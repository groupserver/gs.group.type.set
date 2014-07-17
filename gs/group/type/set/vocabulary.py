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
from operator import attrgetter
from zope.cachedescriptors.property import Lazy
from zope.component import getGlobalSiteManager
from zope.interface.common.mapping import IEnumerableMapping
from zope.schema.vocabulary import SimpleTerm
from .interfaces import ISetType


class GroupTypeVocabulary(object):
    '''The types of group that this group can be set to.'''

    __used_for__ = IEnumerableMapping

    def __init__(self, group):
        self.context = self.group = group

    def __iter__(self):
        """See zope.schema.interfaces.IIterableVocabulary"""
        for a in self.adapters:
            retval = self.adapter_to_term(a)
            yield retval

    def __len__(self):
        """See zope.schema.interfaces.IIterableVocabulary"""
        return len(self.adapterIds)

    def __contains__(self, value):
        """See zope.schema.interfaces.IBaseVocabulary"""
        retval = value in self.adapterIds
        return retval

    def getQuery(self):
        """See zope.schema.interfaces.IBaseVocabulary"""
        return None

    def getTerm(self, value):
        """See zope.schema.interfaces.IBaseVocabulary"""
        return self.getTermByToken(value)

    def getTermByToken(self, token):
        """See zope.schema.interfaces.IVocabularyTokenized"""
        if token in self:
            a = getGlobalSiteManager.getAdapter(self.group, ISetType,
                                                token)
            retval = self.adapter_to_term(a)
            return retval
        raise LookupError(token)

    @staticmethod
    def adapter_to_term(a):
        retval = SimpleTerm(a.typeId, a.typeId, a.name)
        return retval

    @Lazy
    def adapters(self):
        gsm = getGlobalSiteManager()
        adapters = [a[1] for a in gsm.getAdapters((self.group, ), ISetType)
                    if a[1].show]
        retval = sorted(adapters, key=attrgetter('weight'))
        return retval

    @Lazy
    def adaptorIds(self):
        retval = [a.typeId for a in self.adaptors]
        return retval
