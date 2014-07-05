from django.conf import settings
from redis import StrictRedis


r = StrictRedis.from_url(
    getattr(settings, 'REDIS_URL', None),
    max_connections=getattr(settings, 'REDIS_MAX_CONNECTION', None),
)
