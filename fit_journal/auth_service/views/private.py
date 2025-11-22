from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from auth_service.serializers import ChangePasswordRequestSerializer
from utils.constants import APISchemaTags, DefaultAPIResponses


@extend_schema_view(
    post=extend_schema(
        tags=[APISchemaTags.AUTH_SERVICE],
        summary='Сменить пароль',
        operation_id='Сменить пароль',
        request=ChangePasswordRequestSerializer,
        responses={
            **DefaultAPIResponses.RESPONSES,
            status.HTTP_200_OK: {},
        },
    ),
)
class ChangePassword(APIView):
    """
    Сменить пароль
    # todo: переделать на отправку кода подтверждения и возвращение статуса 202
    """

    permission_classes: list = [IsAuthenticated]
    authentication_classes: list = [JWTAuthentication]

    def post(self, reqeust: Request, *args, **kwargs) -> Response:
        """POST-запрос"""
        request_serializer = ChangePasswordRequestSerializer(
            data=reqeust.data,
            context={
                'user': reqeust.user,
            },
        )
        request_serializer.is_valid(raise_exception=True)
        reqeust.user.set_password(request_serializer.validated_data['new_password'])
        return Response(status=status.HTTP_200_OK)
