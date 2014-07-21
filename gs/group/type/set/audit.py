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
SUBSYSTEM = 'gs.group.type.set'
from logging import getLogger
log = getLogger(SUBSYSTEM)
from pytz import UTC
from datetime import datetime
from zope.component.interfaces import IFactory
from zope.interface import implements, implementedBy
from Products.CustomUserFolder.userinfo import userInfo_to_anchor
from Products.GSGroup.groupInfo import groupInfo_to_anchor
from Products.GSAuditTrail import (IAuditEvent, BasicAuditEvent, AuditQuery,
                                   event_id_from_data)
UNKNOWN = '0'
CHANGE_TYPE = '1'


class AuditEventFactory(object):
    implements(IFactory)
    title = 'Change group type audit event factory'
    description = 'Creates a GroupServer audit event for changign a '\
                  'group type'

    def __call__(self, context, event_id, code, date, userInfo,
                 instanceUserInfo, siteInfo, groupInfo, instanceDatum='',
                 supplementaryDatum='', subsystem=''):

        if (code == CHANGE_TYPE):
            event = ChangeTypeEvent(context, event_id, date, userInfo,
                                    siteInfo, groupInfo,
                                    instanceDatum, supplementaryDatum)
        else:
            event = BasicAuditEvent(context, event_id, UNKNOWN, date,
                                    userInfo, instanceUserInfo, siteInfo,
                                    groupInfo, instanceDatum,
                                    supplementaryDatum, SUBSYSTEM)
        assert event
        return event

    def getInterfaces(self):
        return implementedBy(BasicAuditEvent)


class ChangeTypeEvent(BasicAuditEvent):
    """Administrator adding a New User Event.

    The "instanceDatum" is the address used to create the new user.
    """
    implements(IAuditEvent)

    def __init__(self, context, eventId, d, userInfo, siteInfo, groupInfo,
                 toType, fromType):
        super(ChangeTypeEvent, self).__init__(context, eventId, CHANGE_TYPE,
                                              d, userInfo, None, siteInfo,
                                              groupInfo, toType, fromType,
                                              SUBSYSTEM)

    def __unicode__(self):
        r = 'Administrator {0} ({1}) changed the type of the group '\
            '"{2}" ({3}) on "{4}" ({5}) to {6} from {7}'
        retval = r.format(self.userInfo.name, self.userInfo.id,
                          self.groupInfo.name, self.groupInfo.id,
                          self.siteInfo.name, self.siteInfo.id,
                          self.instanceDatum, self.supplementaryDatum)
        return retval

    @property
    def xhtml(self):
        cssClass = 'audit-event gs-group-type-set-{0}'.format(self.code)
        m = '<span class="{cssClass}">Changed the type of {group} '\
            'to {toType} from {fromType}.</span>'
        retval = m.format(cssClass=cssClass,
                          group=groupInfo_to_anchor(self.groupInfo),
                          toType=self.instanceDatum,
                          fromType=self.supplementaryDatum)
        if ((self.instanceUserInfo.id != self.userInfo.id)
                and not(self.userInfo.anonymous)):
            u = userInfo_to_anchor(self.userInfo)
            retval = '{0} &#8212; {1}'.format(retval, u)
        return retval


class Auditor(object):
    def __init__(self, siteInfo, groupInfo, adminInfo):
        self.siteInfo = siteInfo
        self.groupInfo = groupInfo
        self.adminInfo = adminInfo

        self.queries = AuditQuery()
        self.factory = AuditEventFactory()

    def info(self, code, instanceDatum='', supplementaryDatum=''):
        d = datetime.now(UTC)
        eventId = event_id_from_data(self.adminInfo, self.adminInfo,
                                     self.siteInfo, code, instanceDatum,
                                     supplementaryDatum)

        e = self.factory(self.groupInfo.groupObj, eventId, code, d,
                         self.adminInfo, None, self.siteInfo,
                         self.groupInfo, instanceDatum, supplementaryDatum,
                         SUBSYSTEM)
        self.queries.store(e)
        log.info(e)
