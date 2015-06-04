# django-jira-helpdesk
Django Admin App that allows staff users to post &amp; track issues on JIRA without having actual access to it. 

#Installation
Please add "django_jira_helpdesk" to INSTALLED_APPS after "django.contrib.admin"

In URLS please add "url(r'^admin/', include('django_jira_helpdesk.urls')),"
before "url(r'^admin/', include(admin.site.urls)),"

After successful installation please set the following in your settings file:

JIRA_PROJECT_KEY = 'key of project in jira'
JIRA_URL = 'url of your JIRA with port'
#example: 'http://127.0.0.1:8080/'
JIRA_USERNAME = 'JIRA user you want to use"

You can also specify app or site parts that the issue is about.

Be sure to install JIRA python client in your env!

#Features

1. Ability to add, track, comment, upload files JIRA issues in django admin
2. Uses only single JIRA user but tags every issue based on logged in user
3. Upload files to your django static/media files - post them as links in JIRA
4. Runs nicely in Python 3.4