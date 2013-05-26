from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import link, action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework import decorators
from rest_framework import permissions
from rest_framework.authtoken import models
from api.models import Status, Circle, Membership
from api.permissions import IsOwnerOrReadOnly, IsOwner, IsMember
from api.serializers import UserSerializer, StatusSerializer, PasswordSerializer
from api.serializers import CircleSerializer, MemberShipSerializer


class AccountViewSet(viewsets.ViewSetMixin,
                     generics.GenericAPIView):
    serializer_class = PasswordSerializer

    @decorators.permission_reqiured(permission_classes=[permissions.AllowAny, ])
    def user_login(self, request, *args, **kwargs):
        serializer = PasswordSerializer(data=self.request.DATA)
        if serializer.is_valid():
            username, password = serializer.object[
                'username'], serializer.object['password']
            user = get_object_or_404(User, username=username)
            if user.check_password(raw_password=password):
                token = models.Token.objects.get_or_create(user=user)
                return Response("{'token':%s}" % token[0].key)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CircleViewSet(viewsets.ViewSetMixin,
                    generics.GenericAPIView,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    ):

    """
    Present Circle
    """
    model = Circle
    queryset = Circle.objects.all()
    serializer_class = CircleSerializer

    @decorators.permission_reqiured(permission_classes=[permissions.IsAuthenticated])
    def create_circle(self, request, *args, **kwargs):
        return super(mixins.CreateModelMixin, self).create(
            self, request, *args, **kwargs)

    @decorators.permission_reqiured(permission_classes=[IsMember])
    def retrieve_circle(self, request, *args, **kwargs):
        return super(mixins.RetrieveModelMixin, self).retrieve(
            self, request, *args, **kwargs)

    @decorators.permission_reqiured(permission_classes=[IsMember])
    def update_circle(self, request, *args, **kwargs):
        return super(mixins.UpdateModelMixin, self).update(
            self, request, *args, **kwargs)

    def resolve_users(self, request, *args, **kwargs):
        _view = CircleStatusViewSet({'get': 'get_members'}, parent=self)
        return _view(request, *args, **kwargs)

    def resolve_user(self, request, *args, **kwargs):
        _view = CircleStatusViewSet({'get': 'get_membership'}, parent=self)
        return _view(request, *args, **kwargs)

    def resolve_status(self, request, *args, **kwargs):
        _view = CircleStatusViewSet({
                                    'get': 'get_circle_status', 'post': 'add_circle_status'}, parent=self)
        return _view(request, *args, **kwargs)


class CircleUserViewSet(viewsets.ViewSetMixin,
                        generics.GenericAPIView,
                        mixins.SubModelMixin,
                        ):

    """
    Pesent Circle_User
    """

    @decorators.permission_reqiured(permission_classes=[IsMember])
    def get_members(self, request, *args, **kwargs):
        members = self.parent.members.all()
        serializer = UserSerializer(members, many=True)
        return Response(serializer.data)

    @decorators.permission_reqiured(permission_classes=[IsMember])
    def get_membership(self, request, *args, **kwargs):
        membership = Membership.objects.filter_by(
            user=self, circle=self.parent)
        if membership:
            serializer = MemberShipSerializer(membership)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CircleStatusViewSet(viewsets.ViewSetMixin, generics.GenericAPIView,
                          mixins.SubModelMixin):

    @decorators.permission_reqiured(permission_classes=[IsMember])
    def get_circle_status(self, request, *args, **kwargs):
        status = self.parent.status.all()
        serializer = StatusSerializer(status, many=True)
        return Response(serializer.data)

    @decorators.permission_reqiured(permission_classes=[IsMember])
    def add_circle_status(self, request, *args, **kwargs):
        serializer = StatusSerializer(data=self.request.DATA)
        if serializer.is_valid():
            status = serializer.object
            status = serializer.save(force_insert=True)
            status.target_cirlce = self.parent
            status.owner = self.user
            header = {'Location': serializer.data['url']}
            status.save()
            return Response(data=serializer(status), header=header,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ViewSetMixin,
                  generics.GenericAPIView,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @decorators.permission_reqiured(permission_classes=[permissions.IsAuthenticated])
    def retrieve_user(self, request, *args, **kwargs):
        return super(mixins.RetrieveModelMixin, self).update(self, request, *args, **kwargs)

    @decorators.permission_reqiured(permission_classes=[permissions.IsAuthenticated])
    def update_user(self, request, *args, **kwargs):
        return super(mixins.UpdateModelMixin, self).update(self, request, *args, **kwargs)

    @decorators.permission_reqiured(permission_classes=[permissions.IsAuthenticated])
    def destory_user(self, request, *args, **kwargs):
        return super(self, mixins.DestroyModelMixin).destroy(self, request, *args, **kwargs)

    def resolve_status(self, request, *args, **kwargs):
        _view = UserCircleViewSet({'get': 'list_user_status'}, parent=self)
        return _view(request, *args, **kwargs)

    def resolve_circle(self, request, *args, **kwargs):
        _view = UserCircleViewSet({
                                  'get': 'list_user_status', 'put': 'update_user_circle'}, parent=self)
        return _view(request, *args, **kwargs)


class UserStatusViewSet(viewsets.ViewSetMixin, generics.GenericAPIView,
                        mixins.SubModelMixin):

    @decorators.permission_reqiured(permission_classes=[permissions.IsAuthenticated])
    def list_user_status(self, request, *args, **kwargs):
        circle_id = self.request.QUERY_PARAMS.get['circle']
        if circle_id:
            circle = Circle.get_object_or_404(circle_id)
            status = Status.objects.filter_by(
                owner=self.parent, target_circle=circle)
            serializer = StatusSerializer(status, many=True)
            return Response(serializer.data)
        else:
            if self.user == self.parent:
                status = Status.objects.filter_by(owner=self.user)
                serializer = StatusSerializer(status, many=True)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)


class UserCircleViewSet(viewsets.ViewSetMixin, generics.GenericAPIView,
                        mixins.SubModelMixin):

    @decorators.permission_reqiured(permission_classes=[permissions.IsAuthenticated])
    def list_user_circles(self, request, *args, **kwargs):
        serializer = CircleSerializer(self.parent.circles.all())
        return Response(serializer.data)

    @decorators.permission_reqiured(permission_classes=[permissions.IsAuthenticated])
    def update_user_circle(self, request, *args, **kwargs):
        serializer = MemberShipSerializer(self.request.DATA)
        return Response("aaa")
