from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from project_app.models import Project
from django.http import HttpResponse, HttpResponseRedirect
import json


@login_required
def project_manage(request):
    username = request.session.get("user", "")
    project_all = Project.objects.all()
    return render(request, "project_manage.html", {"user": username, "projects": project_all})


@login_required
def search_project(request):
    username = request.session.get("user", "")
    keyword = request.GET.get("keyword", "")
    if keyword == "":
        return HttpResponseRedirect("/manage/project_manage/")
    else:
        result_list = Project.objects.filter(name__contains=keyword)
        return render(request, "project_manage.html", {"user": username, "projects": result_list})


@login_required
def add_project(request):
    new_name = request.POST.get("name", "")
    new_description = request.POST.get("description", "")
    new_status = request.POST.get("status", False)
    if new_status == "on":
        new_status = True
    Project.objects.create(name=new_name, description=new_description, status=new_status)
    return HttpResponseRedirect("/manage/project_manage/")


@login_required
def delete_project(request, project_id):
    target_project = Project.objects.get(id=project_id)
    target_project.delete()
    return HttpResponseRedirect("/manage/project_manage/")


@login_required
def edit_project(request, project_id):      # 编辑时获取数据
    target_project = Project.objects.get(id=project_id)
    response_data = {}
    response_data["name"] = target_project.name
    response_data["description"] = target_project.description
    response_data["status"] = target_project.status
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required
def edit_project_save(request, project_id):  # 保存编辑后的数据
    new_name = request.POST.get("name", "")
    new_description = request.POST.get("description", "")
    new_status = request.POST.get("status", False)
    if new_status == "on":
        new_status = True
    Project.objects.select_for_update().filter(id=project_id).update(name=new_name, description=new_description, status=new_status)
    return HttpResponseRedirect("/manage/project_manage/")
