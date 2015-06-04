import time
from time import mktime
from datetime import datetime
from django import template

register = template.Library()


def style_jira(value):
    if value == "In Progress":
        return 'color: #008000'
    elif value == "Closed":
        return 'text-decoration: line-through;'
    elif value == "Open":
        return 'color: #00F'


def date_jira(value):
        x = time.strptime(value[:-9], '%Y-%m-%dT%H:%M:%S')
        dt = datetime.fromtimestamp(mktime(x))
        return dt.strftime('%H:%M:%S - %d-%m-%Y')


def created_jira_user(value):
    try:
        texts = value.split('<br/>')
        if len(texts) == 2:
            username = texts[1][3:][:-4]
            return ' by {0} '.format(username)
    except Exception as e:
        return ''
    return ''


def comment_jira(value):
    if value[:10] == '#_!FILE!_#':
        rest_of_comment = value[11:].split('<br/>')
        return 'Added file: <a href="{0}">{1}</a>'.format(rest_of_comment[0], rest_of_comment[0].split('/')[-1])
    else:
        try:
            texts = value.split('<br/>')
            if len(texts) == 2:
                username = texts[1][3:][:-4]
                nlen = len(username)
                nlen = -1 * (nlen + 4 + 3 + 5)
                return value[:nlen]
            return value
        except:
            return value
        return value


def jira_color(value):
    if value == 'Critical' or value == 'Major':
        return '#F00'
    elif value == 'Trivial' or value == 'Minor':
        return '#62B662'

register.filter('style_jira', style_jira)
register.filter('date_jira', date_jira)
register.filter('comment_jira', comment_jira)
register.filter('jira_color', jira_color)
register.filter('created_jira_user', created_jira_user)
