class ErrorMiddleware(object):
    """
    Alter HttpRequest objects on Error
    """

    def process_exception(self, request, exception):
        """
        Add user details.
        """
        try:
            request.META['USER_NAME'] = request.user.username
        except:
            request.META['USER_NAME'] = 'Guest'
