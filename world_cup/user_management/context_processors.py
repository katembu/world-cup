from user_management.models import CustomUser, UserMessages


def extra_context(request):
    """
    Add variables that you would like accessed across all pages.

    Author:
         Eric Saupe
    """
    context_extras = {}
    if request.user.is_authenticated():
        user_messages = UserMessages.objects.filter(to=request.user, read=False)
        context_extras['user_messages'] = user_messages

    return context_extras
