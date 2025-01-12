class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print("custom middleware initialized")  # Prints when the middleware is initialized (once during server startup).

    def __call__(self, request):
        print("This is custom Middleware calling")  # Prints for every request.
        response = self.get_response(request)  # Passes the request to the next middleware or view.
        return response  # Returns the response to the client.
