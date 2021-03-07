import logging
from typing import Union

from django.conf import settings
from django.http.request import HttpRequest
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View
from graphene_django.views import GraphQLView
from graphql.execution.base import ExecutionResult
from ratelimit.decorators import ratelimit

from django_graphene_starter.utils import get_client_ip

logger = logging.getLogger(__name__)


@method_decorator(ratelimit(key='user_or_ip', rate=settings.RATELIMIT_RATE, method='GET', block=True), name='get')
class HelloView(View):
    """
    A simple hello world
    """

    def get(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        logger.warning(f'Client with IP Address {get_client_ip(request)} is saying hello!')
        return JsonResponse({'message': 'Hello, 世界!'})


@method_decorator(ratelimit(key='user_or_ip', rate=settings.RATELIMIT_RATE, method=ratelimit.ALL, block=True), name='execute_graphql_request')
class RateLimitedGraphQLView(GraphQLView):
    """
    A basic rate limited GraphQLView
    """

    def execute_graphql_request(self, request: HttpRequest, *args, **kwargs) -> Union[ExecutionResult, None]:
        return super().execute_graphql_request(request, *args, **kwargs)


def ratelimited_error(request: HttpRequest, exception: Exception) -> JsonResponse:
    """
    Returns rate limit error to the client if
    """

    logger.warning(f'Client with IP Address {get_client_ip(request)} is making requests exceeding the rate limit of {settings.RATELIMIT_RATE}!')
    return JsonResponse({'error': 'You are making too many requests! Slow down and enjoy the moment you’re in.'}, status=429)


def custom_page_not_found_view(request: HttpRequest, *args, **kwargs) -> HttpResponse:
    return render(request, '404.html', status=404)
