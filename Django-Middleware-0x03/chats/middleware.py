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
    

    # Store request timestamps per IP in memory
request_log = {}

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.max_requests = 5      # Maximum messages
        self.window_seconds = 60   # 1-minute window

    def __call__(self, request):
        # We only want to limit POST requests (i.e., sending chat messages)
        if request.method == 'POST':
            # Get IP address
            ip = self.get_client_ip(request)
            now = datetime.datetime.now()

            # Initialize list if IP is not seen
            if ip not in request_log:
                request_log[ip] = []

            # Filter out old requests (outside 1-minute window)
            cutoff = now - datetime.timedelta(seconds=self.window_seconds)
            request_log[ip] = [ts for ts in request_log[ip] if ts > cutoff]

            # Check if limit exceeded
            if len(request_log[ip]) >= self.max_requests:
                return HttpResponseForbidden(
                    "Too many messages! You can only send 5 messages per minute."
                )

            # Log the current request time
            request_log[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Extract client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
    
class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Allow only users with role 'admin' or 'moderator'.
        Blocks all other users for protected actions.
        """
        # Only check for authenticated users
        if request.user.is_authenticated:
            # Here we assume the User model has a field named `role`
            # Adjust attribute name if your model uses something else
            user_role = getattr(request.user, "role", None)

            # Check for disallowed roles
            if user_role not in ("admin", "moderator"):
                # Optionally, you can restrict this to certain paths:
                # if request.path.startswith("/chats/"):
                return HttpResponseForbidden("You do not have permission to perform this action.")

        return self.get_response(request)