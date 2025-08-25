import time
from django.utils.deprecation import MiddlewareMixin


class LoggingMiddleware(MiddlewareMixin):
    """
    Custom middleware to log request method, path, and response time.
    """
    
    def process_request(self, request):
        """
        Store the start time of the request.
        """
        request.start_time = time.time()
    
    def process_response(self, request, response):
        """
        Log the request method, path, and response time.
        """
        if hasattr(request, 'start_time'):
            response_time = (time.time() - request.start_time) * 1000  # Convert to milliseconds
            method = request.method
            path = request.path
            
            # Log the information
            print(f"Method: {method}, Path: {path}, Response Time: {response_time:.2f}ms")
        
        return response