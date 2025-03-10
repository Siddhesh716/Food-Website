<<<<<<< HEAD
import logging
from functools import wraps
from django.http import HttpResponse

logger = logging.getLogger('django')

def log_errors(view_func):
    @wraps(view_func)
    def _wrapped_view(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except Exception as e:
            logger.error("An error occurred in view %s: %s", view_func.__name__, e)
            return HttpResponse("An internal server error occurred", status=500)
=======
import logging
from functools import wraps
from django.http import HttpResponse

logger = logging.getLogger('django')

def log_errors(view_func):
    @wraps(view_func)
    def _wrapped_view(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except Exception as e:
            logger.error("An error occurred in view %s: %s", view_func.__name__, e)
            return HttpResponse("An internal server error occurred", status=500)
>>>>>>> 591af9b (Initial commit)
    return _wrapped_view