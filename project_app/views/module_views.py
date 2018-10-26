from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from project_app.models import Module
from django.http import HttpResponse, HttpResponseRedirect
from project_app.forms import ModuleForm


@login_required
def module_manage(request):
    username = request.session.get("user", "")
    module_all = Module.objects.all()
    return render(request, "module_manage.html", {"user": username, "modules": module_all, "type": "list"})


@login_required
def search_module(request):
    username = request.session.get("user", "")
    keyword = request.GET.get("keyword", "")
    print(keyword)
    if keyword == "":
        print(keyword)
        print("keyword is empty")
        return HttpResponseRedirect("/manage/module_manage/")
    else:
        print(keyword)
        print("keyword not empty")
        result_list = Module.objects.filter(name__contains=keyword)
        print(result_list)
        return render(request, "module_manage.html", {"user": username, "modules": result_list, "type": "list"})


@login_required
def add_module(request):
    if request.method == "POST":
        form = ModuleForm(request.POST)
        if form.is_valid():
            new_name = form.cleaned_data["name"]
            new_description = form.cleaned_data["description"]
            new_project = form.cleaned_data["project"]
            Module.objects.create(name=new_name, description=new_description, project=new_project)
        return HttpResponseRedirect("/manage/module_manage/")
    else:
        form = ModuleForm()
    return render(request, "module_manage.html", {"form": form, "type": "add"})


@login_required
def edit_module(request, mid):
    if request.method == "POST":
        form = ModuleForm(request.POST)
        if form.is_valid():
            new_name = form.cleaned_data["name"]
            new_description = form.cleaned_data["description"]
            new_project = form.cleaned_data["project"]
            Module.objects.select_for_update().filter(id=mid).update(name=new_name, description=new_description, project=new_project)
            return HttpResponseRedirect("/manage/module_manage/")
    else:
        if mid:
            form = ModuleForm(instance=Module.objects.get(id=mid))
    return render(request, "module_manage.html", {"form": form, "mid": mid, "type": "edit"})


@login_required
def delete_module(request, mid):
    Module.objects.get(id=mid).delete()
    return HttpResponseRedirect("/manage/module_manage/")

