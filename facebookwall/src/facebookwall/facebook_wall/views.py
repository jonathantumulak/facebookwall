from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django import forms
from django.contrib.auth.forms import UserCreationForm
from wall.forms import UserCreateForm


def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/wall/')
    else:
        return HttpResponseRedirect('/login')


def register(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/login/")
    else:
            form = UserCreateForm()

    return render(request, "register.html", {
        'form': form,
        })
