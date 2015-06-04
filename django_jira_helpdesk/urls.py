# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django_jira_helpdesk.views import admin_helpdesk_view, admin_helpdesk_issue_view, new_issue, \
    add_comment, upload_jira, reopen_issue, close_issue


urlpatterns = patterns('',
    url(r'^helpdesk/$', admin_helpdesk_view, name="admin_helpdesk_view"),
    url(r'^helpdesk/new-issue/$', new_issue, name="new_issue"),
    url(r'^helpdesk/new-comment/$', add_comment, name="add_comment"),
    url(r'^helpdesk/upload/$', upload_jira, name='upload_jira'),
    url(r'^helpdesk/close/$', close_issue, name="close_issue"),
    url(r'^helpdesk/reopen/$', reopen_issue, name="reopen_issue"),
    url(r'^helpdesk/(?P<issue_slug>[-\w]+)/$', admin_helpdesk_issue_view, name="admin_helpdesk_issue_view"),
)
