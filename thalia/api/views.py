from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import link, action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from api.models import Status, Circle, Membership
from api.permissions import IsOwnerOrReadOnly, IsOwner, IsMember
from api.serializers import UserSerializer, StatusSerializer, PasswordSerializer, CircleSerializer



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
        user_status = Status.objects.filter(owner=owner)
        serializer = UserSerializer(user_status, many=True)
        return Response(serializer.data)

    @link()
    def circles(self, request, *args, **kwargs):
        owner = self.get_object()
        serializer = CircleSerializer(owner.circles.all(), many=True)
        return Response(serializer.data)

    permission_classes = (
        permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CircleViewSet(mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.ViewSetMixin,
                    generics.GenericAPIView,
                    ):

    """
    Circle ViewSet
    """
    def get_members(self, request, *args, **kwargs):
        members = self.get_object().members.all()
        serializer = UserSerializer(members, many=True)
        return Response(serializer.data)

    def add_member(self, request, *args, **kwargs):
        added_user_id = self.request.DATA.get('added_user_id')
        if added_user_id:
            added_user = get_object_or_404(User.objects.all(), id=added_user_id)
            ms = Membership(user=added_user, circle=obj)
            ms.save()
            return Response(status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post_save(self, obj, created=True):
        ms = Membership(user=self.request.user, circle=obj)
        ms.save()
    model = Circle
    serializer_class = CircleSerializer
    permission_classes = (IsMember,)
    queryset = Circle.objects.all()

class StatusViewSet(viewsets.ViewSetMixin,
        generics.GenericAPIView,
        mixins.ListModelMixin,
        mixins.DestroyModelMixin,
        ):
    """
    This endpoint presents Code
    """
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = (permissions.IsAdminUser,
                          IsOwner,)


