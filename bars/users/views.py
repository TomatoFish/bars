# coding: utf-8

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.context_processors import csrf


def user_create(request):
    context = {}
    context.update(csrf(request))
    if request.POST:
        username = request.POST.get("username", "")
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        user = User.objects.create_user(username, email, password)
        if user.is_active:
            user.save()
            return HttpResponseRedirect("/")
        else:
            context["creating_error"] = "Не удалось создать пользователя"
            return render_to_response("user-create.html", context)
    else:
        return render_to_response("user-create.html", context)


def login(request):
    context = {}
    context.update(csrf(request))
    if request.POST:
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect("/")
        else:
            context["login_error"] = "Пользователь не найден"
            return render_to_response("login.html", context)
    else:
        return render_to_response("login.html", context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")
