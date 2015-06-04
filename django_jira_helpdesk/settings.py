__author__ = 'Gorman'

JIRA_PROJECT_KEY = 'ECHELP'
JIRA_URL = 'http://83.144.104.54:8080/'
JIRA_USERNAME = 'helpdesk'
JIRA_PASSWORD = 't0eS%sy|f9QFbTOg"QMK'


TYPE_CHOICES = (
                ('Bug', 'Bug'),
                ('New Feature', 'New Feature'),
                ('Improvement', 'Improvement'),
                )
PRIORITY_CHOICES = (
                    ('Trivial', 'Trivial'),
                    ('Minor', 'Minor'),
                    ('Major', 'Major'),
                    ('Critical', 'Critical'),
                    )


MODULE_CHOICES = (
                  ('Admin site', 'Admin site'),
                  ('Blog', 'Blog'),
                  ('CMS and front editing', 'CMS and front editing'),
                  ('General site issues', 'General site issues'),
                  )