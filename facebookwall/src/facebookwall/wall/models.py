import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Status(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User, related_name="status")
    pub_date = models.DateTimeField('date published')
    in_reply_to = models.ForeignKey('self', blank=True,
                                    null=True, default=None,
                                    related_name="replies")

    def __unicode__(self):
        return self.message


class Like(models.Model):
    status = models.ForeignKey(Status, related_name="likes")
    user = models.ForeignKey(User, related_name="likes")

    class Meta:
        unique_together = ['status', 'user']
