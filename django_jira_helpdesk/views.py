# -*- coding: utf-8 -*-
import json
import logging
#Django Imports
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
#Gormanet JIRA Imports
from django_jira_helpdesk.forms import IssueForm, SimpleFileForm
from django_jira_helpdesk.utils import get_jira, sort_issues, get_transitions_id

__author__ = 'Michael Kulaczkowski'

logger = logging.getLogger(__name__)

@login_required
@never_cache
def admin_helpdesk_view(request):
    try:
        jira = get_jira()
        issues = jira.search_issues('project=' + settings.JIRA_PROJECT_KEY)
        for issue in issues:
            issue.comments = jira.comments(issue)[-3:][::-1]
    except Exception as ex:
        logger.error('Cannot pull issues from JIRA: ' + str(ex))
        issues = []

    if 'o' in request.GET:
        sorting = request.GET['o']
        issues = sort_issues(issues, sorting)
    context = {'issues': issues}

    return render_to_response('admin/helpdesk.html', context, context_instance=RequestContext(request))


@login_required
@never_cache
def new_issue(request):
    if request.POST:
        issue_form = IssueForm(request.POST)
        if issue_form.is_valid():
            try:
                jira = get_jira()
                issue_dict = {
                    'project': {'key': settings.JIRA_PROJECT_KEY},
                    'summary': '[' + issue_form.cleaned_data['module_name'] + '] ' + issue_form.cleaned_data['name'],
                    'description': issue_form.cleaned_data['description'],
                    'issuetype': {'name': issue_form.cleaned_data['type']},
                    'priority': {'name': issue_form.cleaned_data['priority']},
                    'labels': [request.user.username]
                    }
                new_issue = jira.create_issue(fields=issue_dict)
                return redirect(reverse('admin_helpdesk_view'))
            except Exception as ex:
                logger.error('Error during new issue creation: ' +str(ex))
                issue_form = None
    else:
        issue_form = IssueForm()

    context = {'form': issue_form}
    return render_to_response('admin/helpdesk_new.html', context, context_instance=RequestContext(request))


@login_required
@never_cache
def admin_helpdesk_issue_view(request, issue_slug):
    e = None
    a = '-'
    issue = None
    commnets = None
    issue_form = None
    try:
        jira = get_jira()
        issue = jira.issue(issue_slug)
        if issue.fields.status.name == 'Closed':
            can_reopen = True
            can_close = False
        else:
            can_reopen = False
            can_close = True
        commnets = jira.comments(issue)
        if request.POST:
            issue_form = IssueForm(request.POST)
            if issue_form.is_valid():
                a = [issue_form.cleaned_data['name'], issue_form.cleaned_data['description'], issue_form.cleaned_data['type'], issue_form.cleaned_data['priority']]
                issue.update(summary=issue_form.cleaned_data['name'],
                             description=issue_form.cleaned_data['description'],
                             issuetype={'name': issue_form.cleaned_data['type']},
                             priority={'name': issue_form.cleaned_data['priority']})
        else:
            data = {
                    'name': issue.fields.summary,
                    'description': issue.fields.description,
                    'type': issue.fields.issuetype.name,
                    'priority': issue.fields.priority.name,
                    }
            issue_form = IssueForm(data)
    except Exception as ex:
        e = ex
        logger.error('Error during JIRA main view generation: ' + str(ex))
    context = {'issue': issue, 'commnets': commnets, 'form': issue_form, 'e': e, 'a': a, 'file_form': SimpleFileForm(), 'can_reopen': can_reopen, 'can_close': can_close}
    return render_to_response('admin/helpdesk_detail.html', context, context_instance=RequestContext(request))


@login_required
@never_cache
def upload_jira(request):
    response_data = {}

    if request.is_ajax():
        form = SimpleFileForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                upload = form.save()
                response_data['status'] = "success"
                response_data['result'] = "Your file has been uploaded:"
                response_data['fileLink'] = "%s" % upload.file.url
                jira = get_jira()
                jira_commnet_formated_for_file = '#_!FILE!_# {0} {1}'
                jira.add_comment(request.POST['issue_slug'], jira_commnet_formated_for_file.format(upload.file.url, user_added(request.user)))

                return HttpResponse(json.dumps(response_data), content_type="application/json")
            except Exception as ex:
                response_data['ex'] = ex
                logger.error('Error during helpdesk file upload: ' + str(ex))
                upload.delete()

    response_data['status'] = "error"
    response_data['result'] = "We're sorry, but something went wrong. Please be sure that your file respects the upload conditions."

    return HttpResponse(json.dumps(response_data), content_type='application/json')


def user_added(user):
    if user.username == 'gormanet':
        return '<br/><b>Helpdesk</b>'
    else:
        return '<br/><b>' + user.username.capitalize() + '</b>'


@login_required
@never_cache
def add_comment(request):
    comment_text = ''
    added_status = 'ERROR'
    if request.POST:
        try:
            jira = get_jira()
            comment_text = request.POST['comment_text'] + user_added(request.user)
            jira.add_comment(request.POST['issue_slug'], comment_text)
            added_status = 'OK'
        except Exception as ex:
            logger.error('Error during adding new comment: ' + str(ex))
            comment_text = ''
            added_status = 'ERROR'
    response_data = {'comment': comment_text, 'status': added_status}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def change_issue(request, issue_status):
    response_data = {}
    try:
        if request.is_ajax():
            if 'issue_slug' in request.POST:
                issue_slug = request.POST['issue_slug']
                jira = get_jira()
                issue = jira.issue(issue_slug)
                transitions = jira.transitions(issue)
                transitions_id = get_transitions_id(issue_status, transitions)
                jira.transition_issue(issue, transitions_id)
                response_data['status'] = 'OK'

            else:
                response_data['error'] = 'No issue_slug'
                response_data['status'] = 'error'
    except Exception as ex:
        response_data['error'] = ex
        response_data['status'] = 'error'
        logger.error('Error during attempt to change issue status: ' + str(ex))
    return response_data


@login_required
@never_cache
def close_issue(request):
    response_data = change_issue(request, 'Close Issue')
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required
@never_cache
def reopen_issue(request):
    response_data = change_issue(request, 'Reopen Issue')
    return HttpResponse(json.dumps(response_data), content_type="application/json")
