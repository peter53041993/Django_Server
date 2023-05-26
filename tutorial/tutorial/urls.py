"""tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth import views as auth_views

router = routers.DefaultRouter()

schema_view = get_schema_view(
    openapi.Info(
        title="TEST_SERVER API",
        default_version='v1',
        description="API DOC",
        terms_of_service="",
        contact=openapi.Contact(email="peter53041993@gmail.com"),
        license=openapi.License(name="Peter"),
    ),
    public=True,
)

urlpatterns = [
    # path('api-user/', include('django.contrib.auth.urls')),
    path('auth-user/login/', auth_views.LoginView.as_view(), name='login'),
    path('admin/', admin.site.urls),
    path("api/", include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

# setting web icon (favicon.ico)
urlpatterns += [
	path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('/favicon.ico'))),
]

urlpatterns += [
    path('', include('snippets.urls')),
    path('', include('ubit_test.urls'))
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]