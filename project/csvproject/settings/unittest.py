from .local import *

# For some reason, the connection pooling causes
# problems with the test runner, something with autocommit...
INSTALLED_APPS = tuple(app for app in INSTALLED_APPS if app != 'djorm_pool')

CELERY_ALWAYS_EAGER = True
