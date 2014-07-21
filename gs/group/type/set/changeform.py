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
from zope.cachedescriptors.property import Lazy
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from zope.component import getGlobalSiteManager
from gs.content.form.base import radio_widget
from gs.core import to_ascii
from gs.group.base import GroupForm
from .audit import (Auditor, CHANGE_TYPE)
from .interfaces import (IChangeGroupType, ISetType, IUnsetType)


class ChangeGroupType(GroupForm):
    'The Change Group Type page view'
    label = 'Change group type'
    pageTemplateFileName = to_ascii('browser/templates/form.pt')
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)
    interface = IChangeGroupType

    @Lazy
    def form_fields(self):
        form_fields = form.Fields(self.interface, render_context=False)
        form_fields['groupType'].custom_widget = radio_widget
        return form_fields

    def setUpWidgets(self, ignore_request=False):
        currentType = IUnsetType(self.context).setTypeId
        data = {'groupType': currentType}
        self.widgets = form.setUpWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            form=self, data=data, ignore_request=ignore_request)

    @staticmethod
    def a_or_an(s):
        return 'an' if (s[0] in 'aeiou') else 'a'

    @form.action(label='Change', failure='handle_change_action_failure')
    def handle_change(self, action, data):
        # Note that it is importtant to get the setter and unsetter *before*
        # calling unset. After unset is called the group is (briefly) not
        # a group, so the adapter will fail.
        unsetter = IUnsetType(self.context)
        gsm = getGlobalSiteManager()
        setter = gsm.getAdapter(self.context, ISetType, data['groupType'])

        unsetter.unset()
        setter.set()

        # The name of the group-type in the setter is long, so get the
        # short-name from a new unsetter.
        newType = IUnsetType(self.context).name.lower()
        oldType = unsetter.name.lower()
        auditor = Auditor(self.siteInfo, self.groupInfo, self.loggedInUser)
        auditor.info(CHANGE_TYPE, newType, oldType)
        s = 'Changed {0} <strong>to {1} {2}</strong> from {3} {4}.'
        self.status = s.format(self.groupInfo.name, self.a_or_an(newType),
                               newType, self.a_or_an(oldType), oldType)

    def handle_change_action_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = '<p>There is an error:</p>'
        else:
            self.status = '<p>There are errors:</p>'
        self.status = data
