from django import template
from user_management.models import UserMessages

register = template.Library()


@register.filter
def get_messages(user):
    return UserMessages.objects.filter(to=user)


@register.filter
def get_reply_messages(message):
    messages = []
    while message.reply_to:
        messages.append(message.reply_to)
        message = message.reply_to
    return messages
