from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from interface_app.models import TestCase
from project_app.models import Project, Module
import requests
import json


@login_required
def case_manage(request):
    if request.method == "GET":
        case_all = TestCase.objects.all()
        paginator = Paginator(case_all, 3)
        page = request.GET.get("page")
        try:
            cases = paginator.page(page)
        except PageNotAnInteger:
            cases = paginator.page(1)
        except EmptyPage:
            cases = paginator.page(paginator.num_pages)

        return render(request, "case_manage.html", {
            "cases": cases,
            "type": "list"
        })
    else:
        return HttpResponse("404")


@login_required
def search_case(request):
    if request.method == "GET":
        keyword = request.GET.get("keyword", "")
        result_list = TestCase.objects.filter(name__contains=keyword)

        paginator = Paginator(result_list, 3)
        page = request.GET.get("page")
        try:
            cases = paginator.page(page)
        except PageNotAnInteger:
            cases = paginator.page(1)
        except EmptyPage:
            cases = paginator.page(paginator.num_pages)

        return render(request, "case_manage.html", {
            "cases": cases,
            "type": "list",
            "keyword": keyword,
        })

    else:
        return HttpResponse("404")


@login_required
def get_projects_and_modules(request):
    projects = Project.objects.all()
    project_list = []
    for project in projects:
        current_project = {"projectName": project.name}
        modules = Module.objects.filter(project_id=project.id)
        if len(modules) != 0:
            module_names = []
            for module in modules:
                module_names.append(module.name)
            current_project["moduleNames"] = module_names

        project_list.append(current_project)

    return JsonResponse({"projects": project_list})


@login_required
def debug_case(request):
    if request.method == "POST":
        url = request.POST.get("url")
        method = request.POST.get("method")
        param_type = request.POST.get("paramType")
        headers = json.loads(request.POST.get("headers").replace("'", "\""))
        params = json.loads(request.POST.get("params").replace("'", "\""))
        if method == "get":
            r = requests.get(url, params=params, headers=headers)

        if method == "post":
            if param_type == "form-data":
                r = requests.post(url, data=params, headers=headers)
            if param_type == "json":
                r = requests.post(url, json=params, headers=headers)

        return HttpResponse(r.text)
    else:
        return render(request, "api_debug.html", {
            "type": "debug"
        })


@login_required
def save_case(request):
    if request.method == "POST":
        module_name = request.POST.get("moduleName", "")
        name = request.POST.get("name", "")
        url = request.POST.get("url", "")
        method = request.POST.get("method", "").upper()
        param_type = request.POST.get("paramType", "")
        headers = request.POST.get("headers", "{}")
        params = request.POST.get("params", "{}")

        if module_name == "" or name == "" or url == "" or method == "" or param_type == "":
            return JsonResponse({"isSuccessful": "false", "message": "模块名、用例名、url、请求方法、请求参数类型不能为空！"})

        module = Module.objects.get(name=module_name)

        test_case = TestCase.objects.create(module=module,
                                            name=name,
                                            url=url,
                                            request_method=method,
                                            request_headers=headers,
                                            request_params_type=param_type,
                                            request_params=params)

        if test_case is not None:
            return JsonResponse({"isSuccessful": "true", "message": "保存成功！"})
        else:
            return JsonResponse({"isSuccessful": "false", "message": "未知错误！保存失败！"})

    else:
        return HttpResponse("404")


@login_required
def delete_case(request, case_id):
    TestCase.objects.get(id=case_id).delete()
    return HttpResponseRedirect("/interface/case_manage/")