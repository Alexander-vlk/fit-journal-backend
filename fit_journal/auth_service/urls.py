from django.urls import path

from auth_service.views import HealthCheck

urlpatterns = [
    path('healthcheck/', HealthCheck.as_view(), name='health_check'),
]
