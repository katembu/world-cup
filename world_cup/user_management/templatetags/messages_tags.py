from django import template
from user_management.models import UserMessages

register = template.Library()


@register.filter
def get_messages(user):
    return UserMessages.objects.filter(to=user)
