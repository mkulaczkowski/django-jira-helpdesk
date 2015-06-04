# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Upload'
        db.create_table('django_jira_helpdesk_upload', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=256)),
        ))
        db.send_create_signal('django_jira_helpdesk', ['Upload'])


    def backwards(self, orm):
        # Deleting model 'Upload'
        db.delete_table('django_jira_helpdesk_upload')


    models = {
        'django_jira_helpdesk.upload': {
            'Meta': {'object_name': 'Upload'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['django_jira_helpdesk']