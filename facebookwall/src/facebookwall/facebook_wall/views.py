from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django import forms
from django.contrib.auth.forms import UserCreationForm


def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/logged_in')
    else:
        return HttpResponseRedirect('/login')


@login_required
def logged_in(request):
    return render_to_response(
        'logged_in.html',
        context_instance=RequestContext(request)
    )


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/login/")
    else:
            form = UserCreationForm()

    return render(request, "register.html", {
        'form': form,
        })
