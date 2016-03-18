from django import template
from application.models import Vote
register = template.Library()


@register.simple_tag
def get_vote(app, judge):
    try:
        return Vote.objects.get(user=judge, application=app).point
    except:
        return "-"
