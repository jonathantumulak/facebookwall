from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django import forms
from django.views import generic

from wall.forms import UserCreateForm
from wall.models import User


class IndexView(generic.View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/wall/')
        else:
            return HttpResponseRedirect('/login')


class RegisterView(generic.CreateView):
    model = User
    form_class = UserCreateForm
    fields = ['username', 'email', 'first_name',
              'last_name', 'password']
    template_name = 'register.html'
    success_url = '/login/'
