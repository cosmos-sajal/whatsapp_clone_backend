"""
Middleware to log all requests and responses.
Uses a logger configured by the name of django.request
to log all requests and responses according to configuration
specified for django.request.
Reference -
https://gist.github.com/SehgalDivij/1ca5c647c710a2c3a0397bce5ec1c1b4
"""
import json
import logging
import socket
import time

from django.utils.deprecation import MiddlewareMixin

request_logger = logging.getLogger('django.request')


class RequestLogMiddleware(MiddlewareMixin):
    """Request Logging Middleware."""

    def __init__(self, *args, **kwargs):
        """Constructor method."""
        super().__init__(*args, **kwargs)

    def process_request(self, request):
        """Set Request Start Time to measure time taken to service request."""

        if request.method in ['POST', 'PUT', 'PATCH']:
            request.req_body = request.body
        if str(request.get_full_path()).startswith('/api/'):
            request.start_time = time.time()

    def extract_log_info(self, request, response=None, exception=None):
        """Extract appropriate log info from requests/responses/exceptions."""

        if hasattr(request, 'user'):
            user = str(request.user)
        else:
            user = None

        log_data = {
            'remote_address': request.META['REMOTE_ADDR'],
            'server_hostname': socket.gethostname(),
            'request_method': request.method,
            'request_path': request.get_full_path(),
            'run_time': time.time() - request.start_time,
            'user_id': user,
            'status_code': response.status_code
        }

        try:
            if request.method in ['PUT', 'POST', 'PATCH'] and \
                    request.req_body != b'':
                log_data['request_body'] = json.loads(
                    str(request.req_body, 'utf-8'))
        except Exception:
            log_data['request_body'] = 'error parsing'

        try:
            if response:
                if response['content-type'] == 'application/json':
                    response_body = response.content
                    log_data['response_body'] = json.loads(response_body)
        except Exception:
            log_data['request_body'] = 'error parsing'

        return log_data

    def process_response(self, request, response):
        """Log data using logger."""
        if str(request.get_full_path()).startswith('/api/'):
            log_data = self.extract_log_info(request=request,
                                             response=response)
            request_logger.info(msg=log_data, extra=log_data)

        return response

    def process_exception(self, request, exception):
        """Log Exceptions."""
        try:
            raise exception
        except Exception:
            request_logger.exception(msg="Unhandled Exception")
        return exception
