from django.db import models


class Upload(models.Model):
    """
    This models holds path to files uploaded to static file server
    """
    file = models.FileField(upload_to="uploaded_to_jira/", max_length=256)

    class Meta:
        app_label = 'django_jira_helpdesk'
        verbose_name = 'File'
        verbose_name_plural = 'Files'
