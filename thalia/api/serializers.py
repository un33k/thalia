from rest_framework import serializers
from api.models import Circle, Status
from django.contrib.auth.models import User


class CircleSerializer(serializers.HyperlinkedModelSerializer):
    members = serializers.HyperlinkedIdentityField(view_name='circle-members')
    status = serializers.HyperlinkedIdentityField(view_name='circle-status')

    class Meta:
        model = Circle
        fields = ('url', 'circlename', 'description',
                  'created', 'members', 'status')


class StatusSerializer(serializers.HyperlinkedModelSerializer):
    owner_name = serializers.Field(source='owner.username')
    # owner = serializers.HyperlinkedIdentityField(view_name='user-detail')
    target_circle_name = serializers.Field(source='target_circle.circlename')
    # target_circle = serializers.HyperlinkedIdentityField(
    #    view_name='circle-detail')

    class Meta:
        model = Status
        fields = ('url', 'owner_name', 'owner',
                  'target_circle_name', 'target_circle',
                  'content', 'image_url', 'style', 'created')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    status = serializers.HyperlinkedIdentityField(view_name="user-status")
    # circles = serializers.HyperlinkedIdentityField(
    #    view_name='user-circles')

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'status')


class PasswordSerializer(serializers.Serializer):

    """
    Used as User Controll
    """
    email = serializers.EmailField()
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=16)
