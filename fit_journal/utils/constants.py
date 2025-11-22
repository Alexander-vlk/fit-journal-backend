from drf_spectacular.utils import OpenApiResponse
from rest_framework import status


class APISchemaTags:
    """Теги АПИ"""

    AUTH_SERVICE = 'Сервис аутентификации'
    JOURNAL = 'Дневник тренировок'

class DefaultAPIResponses:
    """Ответы сервера по умолчанию"""

    _success_text = 'Стандартный ответ при успешном ответе'
    _bad_request_error_text = 'Описание ошибки валидации'
    _unauthorized_error_text = 'Учетные данные не были предоставлены'
    _access_denied = 'У вас нет прав на выполнение этого действия'
    _not_found_error_text = 'Страница не найдена'
    _method_not_allowed_error_text = 'Метод <method> не разрешён для этого ресурса'
    _internal_server_error_text = 'Произошла внутренняя ошибка сервера'

    RESPONSES = {
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(description=_bad_request_error_text),
        status.HTTP_401_UNAUTHORIZED: OpenApiResponse(description=_unauthorized_error_text),
        status.HTTP_403_FORBIDDEN: OpenApiResponse(description=_access_denied),
        status.HTTP_404_NOT_FOUND: OpenApiResponse(description=_not_found_error_text),
        status.HTTP_405_METHOD_NOT_ALLOWED: OpenApiResponse(description=_method_not_allowed_error_text),
        status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(description=_internal_server_error_text),
    }
