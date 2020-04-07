from django import template

register = template.Library()

@register.filter
def get_notifications(user):
    return user.notifications.filter(read=False,deleted=False).count()