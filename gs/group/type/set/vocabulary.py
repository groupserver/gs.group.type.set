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
        for a in self.adaptors:
            retval = self.adaptor_to_term(*a)
            yield retval

    def __len__(self):
        """See zope.schema.interfaces.IIterableVocabulary"""
        return len(self.adaptorIds)

    def __contains__(self, value):
        """See zope.schema.interfaces.IBaseVocabulary"""
        retval = value in self.adaptorIds
        return retval

    def getQuery(self):
        """See zope.schema.interfaces.IBaseVocabulary"""
        return None

    def getTerm(self, value):
        """See zope.schema.interfaces.IBaseVocabulary"""
        return self.getTermByToken(value)

    def getTermByToken(self, token):
        """See zope.schema.interfaces.IVocabularyTokenized"""
        if token not in self:
            raise LookupError(token)
        gsm = getGlobalSiteManager()
        a = gsm.getAdapter(self.group, ISetType, token)
        retval = self.adaptor_to_term(token, a)
        return retval

    @staticmethod
    def adaptor_to_term(token, a):
        retval = SimpleTerm(token, token, a.name)
        return retval

    @Lazy
    def adaptors(self):
        gsm = getGlobalSiteManager()
        adaptors = [a for a in gsm.getAdapters((self.group, ), ISetType)
                    if a[1].show]
        retval = sorted(adaptors, key=lambda a: a[1].weight)
        return retval

    @Lazy
    def adaptorIds(self):
        retval = [a[0] for a in self.adaptors]
        return retval
