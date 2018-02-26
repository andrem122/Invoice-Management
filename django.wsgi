import os
import sys

path='/var/www/html/django-apps/project_management'

if path not in sys.path:
  sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'project_management.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandlyer()
