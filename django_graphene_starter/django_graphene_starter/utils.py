from typing import Union

from django.http import HttpRequest


def get_client_ip(request: HttpRequest) -> Union[str, None]:
    """
    Get the Client's IP address from request headers
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
