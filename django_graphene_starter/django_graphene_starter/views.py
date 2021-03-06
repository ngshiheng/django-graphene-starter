from django.conf import settings
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from graphene_django.views import GraphQLView
from ratelimit.decorators import ratelimit


@method_decorator(ratelimit(key='ip', rate=settings.RATELIMIT_RATE, method=ratelimit.ALL, block=True), name='execute_graphql_request')
class RateLimitedGraphQLView(GraphQLView):
    """
    A basic rate limited GraphQLView
    """

    def execute_graphql_request(self, request, *args, **kwargs):
        return super().execute_graphql_request(request, *args, **kwargs)


def ratelimited_error(request, exception):
    return JsonResponse({'error': 'You are making too many requests! Slow down and enjoy the moment you’re in.'}, status=429)
