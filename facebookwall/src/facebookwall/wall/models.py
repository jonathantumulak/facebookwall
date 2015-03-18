from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime


class Status(models.Model):
    message = models.CharField(max_length=200)
    author = models.ForeignKey(User, related_name="author")
    pub_date = models.DateTimeField('date published')
    in_reply_to = models.ForeignKey('self')


class Likes(models.Model):
    liked_status = models.ForeignKey(Status, related_name="liked")
    liker = models.ForeignKey(User, related_name="liker")
