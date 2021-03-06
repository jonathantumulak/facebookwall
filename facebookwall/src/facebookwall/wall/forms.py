from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from django.utils import timezone

from wall.models import Status


class StatusForm(ModelForm):
    message = forms.CharField(widget=forms.Textarea, label='')

    class Meta:
        model = Status
        exclude = ['user', 'pub_date', 'in_reply_to']

    def __init__(self, *args, **kwargs):
        super(StatusForm, self).__init__(*args, **kwargs)
        self.fields['message'].widget.attrs.update({
                'class': 'form-control',
                'id': 'message-content',
                'rows': 2,
                'placeholder': 'What\'s on your mind?',
                'required': 'true',
            })


class ReplyForm(ModelForm):
    message = forms.CharField(widget=forms.Textarea, label='')

    class Meta:
        model = Status
        exclude = ['user', 'pub_date', 'in_reply_to']

    def __init__(self, *args, **kwargs):
        super(ReplyForm, self).__init__(*args, **kwargs)
        self.fields['message'].widget.attrs.update({
                'class': 'form-control',
                'id': 'message-content',
                'rows': 2,
                'placeholder': 'Write a comment...',
                'required': 'true',
            })


class PostStatusForm(StatusForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(StatusForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        status = super(PostStatusForm, self).save(commit=False)
        status.user = self.user
        status.pub_date = timezone.now()

        if commit:
            status.save()
        return status


class PostReplyForm(StatusForm):
    def __init__(self, user, reply_to, *args, **kwargs):
        self.user = user
        self.reply_to = reply_to
        super(StatusForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        status = super(PostReplyForm, self).save(commit=False)
        status.user = self.user
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
