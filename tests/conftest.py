import django
from django.conf import settings
from django.db import connection

def pytest_sessionfinish(session, exitstatus):
    django.setup()
    connection.close()
    connection.settings_dict["NAME"] = settings.DATABASES["default"]["NAME"]
