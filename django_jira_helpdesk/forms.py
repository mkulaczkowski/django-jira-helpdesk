from django import forms
from django_jira_helpdesk.models.files_upload import Upload
from django_jira_helpdesk.settings import MODULE_CHOICES, TYPE_CHOICES, PRIORITY_CHOICES


class IssueForm(forms.Form):
    """
    Form responsbile for adding new issues in JIRA
    """

    module_name = forms.CharField(widget=forms.Select(choices=MODULE_CHOICES))
    name = forms.CharField(label="Issue Name",)
    type = forms.CharField(label="Issue Type", widget=forms.Select(choices=TYPE_CHOICES))
    priority = forms.CharField(label="Priority", widget=forms.Select(choices=PRIORITY_CHOICES))
    description = forms.CharField(label="Description", widget=forms.Textarea())


class SimpleFileForm(forms.ModelForm):
    class Meta:
        model = Upload
