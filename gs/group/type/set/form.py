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
from gs.content.form.base import radio_widget
from gs.core import to_ascii
from gs.group.base import GroupForm
from .interfaces import IChangeGroupType


class ChangeGroupType(GroupForm):
    'The Change Group Type page view'
    label = 'Change the group type'
    pageTemplateFileName = to_ascii('browser/templates/form.pt')
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)
    form_fields = form.Fields(IChangeGroupType, render_context=False)

    @Lazy
    def form_fields(self):
        form_fields = form.Fields(self.interface, render_context=True)
        form_fields['groupType'].custom_widget = radio_widget
        return form_fields

    def setUpWidgets(self, ignore_request=False):
        # TODO: Set the current group-type up as the default
        self.widgets = form.setUpWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            form=self, ignore_request=ignore_request)

    @form.action(label='Change', failure='handle_change_action_failure')
    def handle_change(self, action, data):
        self.status = 'Foo'

    def handle_change_action_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = '<p>There is an error:</p>'
        else:
            self.status = '<p>There are errors:</p>'
