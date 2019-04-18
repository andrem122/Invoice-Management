from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from jobs.models import House
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)
