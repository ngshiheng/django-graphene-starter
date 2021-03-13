import logging
from typing import Union

from django.http import HttpRequest
from graphene import ResolveInfo

logger = logging.getLogger(__name__)


def get_client_ip(request: HttpRequest) -> Union[str, None]:
    """
    Get the Client's IP address from request headers
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')


def get_operation_info(func):
    """
    A decorator use to log GraphQL operation information from ResolveInfo

    Example usage:

    ```python

    @classmethod
    @get_operation_info
    def mutate_and_get_payload(cls, root, info: ResolveInfo, **input) -> 'Mutation':
        # ...
    ```
    """
    def wrap(cls, root, info: ResolveInfo, **kwargs):
        query_information = {
            'operation_type': info.operation.operation,
            'operation_name': info.operation.name.value,
            'query': info.operation.selection_set.selections[0].name.value,
        }

        logger.debug(query_information)
        return func(cls, root, info, **kwargs)
    return wrap
