__author__ = 'Michael Kulaczkowski'
from jira.client import JIRA
from django.conf import settings

def get_jira():
    """
    This returns JIRA object - please look here for details -> http://jira-python.readthedocs.org/en/latest/
    """
    return JIRA(basic_auth=(settings.JIRA_USERNAME, settings.JIRA_PASSWORD), options={'verify': False, 'server': settings.JIRA_URL})


def get_transitions_id(transition_name, transitions_list):
    """
    Function return ID of transition
    """
    for transition in transitions_list:
        if transition['name'] == transition_name:
            return transition['id']
    return None


def sort_issues(issues, sorting):
    if sorting == '1':
        return sorted(issues, key=lambda x: x.fields.summary)
    elif sorting == '2':
        return sorted(issues, key=lambda x: x.fields.status.name, reverse=True)
    elif sorting == '3':
        return sorted(issues, key=lambda x: x.fields.priority.name)
    elif sorting == '4':
        return sorted(issues, key=lambda x: x.fields.issuetype.name)
    elif sorting == '5':
        return sorted(issues, key=lambda x: x.fields.description)
    return issues
