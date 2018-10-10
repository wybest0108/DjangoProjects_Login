from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from user_app.models import Project, Module

# Create your views here.


def index(request):
    return render(request, 'index.html')


def login_action(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        if username == "" or password == "":
            return render(request, "index.html", {"error": "用户名或者密码为空"})
        else:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                request.session["user"] = username
                return HttpResponseRedirect("/project_manage/")
            else:
                return render(request, "index.html", {"error": "用户名或者密码错误"})


@login_required
def project_manage(request):
    username = request.session.get("user", "")
    project_all = Project.objects.all()
    return render(request, "project_manage.html", {"user": username, "projects": project_all})


@login_required
def module_manage(request):
    username = request.session.get("user", "")
    module_all = Module.objects.all()
    return render(request, "module_manage.html", {"user": username, "modules": module_all})


def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect("/")
    return response
