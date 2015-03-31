import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Status(models.Model):
    message = models.TextField()
    author = models.ForeignKey(User, related_name="author")
    pub_date = models.DateTimeField('date published')
    in_reply_to = models.ForeignKey('self', blank=True,
                                    null=True, default=None,
                                    related_name="replies")

    def __unicode__(self):
        return self.message


class Likes(models.Model):
    class Meta:
        unique_together = ['liked_status', 'liker']
    liked_status = models.ForeignKey(Status, related_name="liked")
    liker = models.ForeignKey(User, related_name="liker")
