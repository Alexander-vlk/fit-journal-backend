from django.urls import path

from auth_service.views import HealthCheck, CustomTokenObtainPairView, CustomTokenRefreshView, ChangePassword

urlpatterns = [
    path('healthcheck/', HealthCheck.as_view(), name='health_check'),
    path('token/obtain/', CustomTokenObtainPairView.as_view(), name='token_obtain'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('password/change/', ChangePassword.as_view(), name='password_change'),
]
