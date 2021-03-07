from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from django_graphene_starter.views import HelloView, RateLimitedGraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql', csrf_exempt(RateLimitedGraphQLView.as_view(graphiql=True))),
    path('hello', HelloView.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


handler404 = 'django_graphene_starter.views.custom_page_not_found_view'
