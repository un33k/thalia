from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Circle(models.Model):

    """ The Circle"""
    circlename = models.CharField(max_length=20)
    description = models.CharField(max_length=120, blank=True)
    members = models.ManyToManyField(
        User, related_name='circles', through="Membership")
    created = models.DateTimeField(auto_now_add=True)


class Status(models.Model):

    """The Status"""
    STATUS_STYLES = [("1", "text"), ("2", "image")]
    content = models.TextField()
    owner = models.ForeignKey(User, related_name="status")
    style = models.CharField(choices=STATUS_STYLES, max_length="20")
    image_url = models.URLField(blank=True)
    target_circle = models.ForeignKey(Circle, related_name="status")
    created = models.DateTimeField(auto_now_add=True)


class Membership(models.Model):

    """The Relation Between Circle And Users"""
    STAGES = [("1", "owner"), ("2", "common")]
    stage = models.CharField(choices=STAGES, max_length=20)
    user = models.ForeignKey(User)
    circle = models.ForeignKey(Circle)
