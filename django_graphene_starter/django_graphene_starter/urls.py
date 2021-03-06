from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from django_graphene_starter.views import RateLimitedGraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql', csrf_exempt(RateLimitedGraphQLView.as_view(graphiql=True))),
]
