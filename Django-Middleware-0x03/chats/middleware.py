import datetime

from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_entry = f"{datetime.datetime.now()} - User: {user} - Path: {request.path}\n"

        with open("requests.log", "a") as log_file:
            log_file.write(log_entry)

        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Current hour (0-23)
        current_hour = datetime.datetime.now().hour

        # Allow only between 6 (06:00) and 21 (21:00)
        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden("Chat access is restricted during this time.")

        return self.get_response(request)