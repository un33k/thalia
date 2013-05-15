from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import link, action
from rest_framework.response import Response
from rest_framework import status
from api.models import Status, Circle
from api.permissions import IsOwnerOrReadOnly, IsOwner, IsMember
from api.serializers import UserSerializer, StatusSerializer, PasswordSerializer


class StatusViewSet(viewsets.ModelViewSet):

    """
    This endpoint presents Code
    """
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def pre_save(self, obj):
        obj.owner = self.request.user


class UserViewSet(viewsets.ModelViewSet):

    """
    This endpoint presents User
    """

    @action(permission_classes=[IsOwner])
    def password(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.DATA)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return Response("'status': 'success'")
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @link(permission_classes=[IsOwnerOrReadOnly])
    def status(self, request, *args, **kwargs):
        owner = self.get_object()
        user_status = Circle.objects.filter(owner=owner)
        serializer = UserSerializer(user_status, many=True)
        return Response(serializer.data)
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
