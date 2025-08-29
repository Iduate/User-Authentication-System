class AuthorizationHeaderMiddleware:
    """
    Middleware to convert Authorization header to HTTP_AUTHORIZATION.
    Django converts headers by prepending HTTP_ and converting dashes to underscores,
    but sometimes this doesn't work correctly with certain setups.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'Authorization' in request.headers and 'HTTP_AUTHORIZATION' not in request.META:
            request.META['HTTP_AUTHORIZATION'] = request.headers['Authorization']
        return self.get_response(request)
