"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg       import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="모두의 대결",
        default_version='1.1.1',
        description="모두의 대결 API 문서",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    # path(r'swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'api/swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'api/redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
    path("api/admin/", admin.site.urls),
    path("api/user/", include("users.urls")),
    
]
