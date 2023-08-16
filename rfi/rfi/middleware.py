

class CorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Access-Control-Allow-Origin'] = 'http://localhost:8080'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response