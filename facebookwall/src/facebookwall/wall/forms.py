from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from wall.models import Status
from django.utils import timezone


class StatusForm(ModelForm):
    class Meta:
        model = Status
        exclude = ['author', 'pub_date', 'in_reply_to']


class PostStatusForm(StatusForm):
    def __init__(self, user, *args, **kwargs):
        self.author = user
        super(StatusForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        status = super(PostStatusForm, self).save(commit=False)
        status.author = self.author
        status.pub_date = timezone.now()

        if commit:
            status.save()
        return status


class PostReplyForm(StatusForm):
    def __init__(self, user, reply_to, *args, **kwargs):
        self.author = user
        self.reply_to = reply_to
        super(StatusForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        status = super(PostReplyForm, self).save(commit=False)
        status.author = self.author
        status.pub_date = timezone.now()
        status.in_reply_to = Status.objects.get(pk=self.reply_to)

        if commit:
            status.save()
        return status


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user
