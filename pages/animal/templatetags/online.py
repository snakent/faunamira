from django import template
from django.utils.timezone import now
register = template.Library()

@register.filter
def online(lasttime):
    if lasttime:
        timediff = now() - lasttime
        if timediff.total_seconds()<600:
            return True
    return None