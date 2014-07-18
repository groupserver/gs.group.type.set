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
    '''The types of group that a group can be set to.

:param group: The group-folder.

The :class:`GroupTypeVocabulary` vocabulary lists all the *adaptors* for
the current ``group`` that can be used to *set* the group to a particular
type.
'''
    __used_for__ = IEnumerableMapping

    def __init__(self, group):
        self.context = self.group = group

    def __iter__(self):
        """Iterate through all the *adaptors* that set the type of the group

:returns: The adaptors for the group-folder that provide the
          :class:`gs.group.type.set.interfaces.ISetType` interface.
:rtype: Instances of the :class:`zope.schema.vocabulary.SimpleTerm` class.
"""
        for a in self.adaptors:
            retval = self.adaptor_to_term(*a)
            yield retval

    def __len__(self):
        """The number of adaptors in the vocabulary"""
        return len(self.adaptorIds)

    def __contains__(self, value):
        """Does the vocabulary contain a particular adaptor """
        retval = value in self.adaptorIds
        return retval

    def getQuery(self):
        """See :class:`zope.schema.interfaces.IBaseVocabulary`"""
        return None

    def getTerm(self, value):
        """See :class:`zope.schema.interfaces.IBaseVocabulary`"""
        return self.getTermByToken(value)

    def getTermByToken(self, token):
        """See :class:`zope.schema.interfaces.IVocabularyTokenized`"""
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
        '''The named adaptors that provide the ``ISetType`` interface.

:returns: The named adaptors that provide the
          :class:`gs.group.type.set.interfaces.ISetType`interface, sorted
          by the ``weight`` of each adaptor.
:rtype: list.'''
        gsm = getGlobalSiteManager()
        adaptors = [a for a in gsm.getAdapters((self.group, ), ISetType)
                    if a[1].show]
        retval = sorted(adaptors, key=lambda a: a[1].weight)
        return retval

    @Lazy
    def adaptorIds(self):
        '''The identifiers (*names*) of the named adaptors

:returns: The names of the named adaptors, in the same order as returned by
          :attr:`adaptors`.
:rtype: string'''
        retval = [a[0] for a in self.adaptors]
        return retval
