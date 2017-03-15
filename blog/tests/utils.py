from datetime import datetime as original_datetime

from django.conf import settings
from django.utils import timezone


def omniscient_datetime(*args):
    '''
    Generating a datetime aware or naive depending of USE_TZ
    '''
    d = original_datetime(*args)
    if settings.USE_TZ:
        d = timezone.make_aware(d, timezone.utc)
    return d

datetime = omniscient_datetime