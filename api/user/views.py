
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions
from .serializers import AuthTokenSerializer
from django.contrib.auth import login


class LoginView(KnoxLoginView):
    """
    Login User to system
    requrest format : {
        'email':'test@gmail.com',
        'password':'somepassoword'
    }
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super(LoginView, self).post(request, format=None)