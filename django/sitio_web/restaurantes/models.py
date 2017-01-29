from __future__ import unicode_literals
from django.conf import settings

mongo_client = settings.CLIENT
db = mongo_client.test
