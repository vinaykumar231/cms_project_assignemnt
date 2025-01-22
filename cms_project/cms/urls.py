from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Schema view for Swagger UI
schema_view = get_schema_view(
    openapi.Info(
        title="CMS API",
        default_version='v1',
        description="CMS API documentation",
        contact=openapi.Contact(email="contact@cmsapi.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# Homepage redirection to Swagger
def homepage(request):
    return HttpResponseRedirect('/swagger/')

# URL patterns
urlpatterns = [
    path('', homepage),  # Redirect from home to Swagger UI
    path('admin/', admin.site.urls),  # Admin panel
    path('api/auth/', include('users.urls')),  # Authentication-related API routes
    path('api/content/', include('content.urls')),  # Content-related API routes
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),  # Swagger UI for API docs
]
