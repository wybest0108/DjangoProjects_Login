from django.contrib.auth.decorators import login_required
from interface_app.models import TestCase, TestTask
from project_app.models import Project, Module
from test_platform.common import response_succeed, response_fail
import requests
import json


@login_required
def save_task(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        if(name == ""):
            return response_fail("任务名称不能为空！")

        description = request.POST.get("description", "")
        case_ids = request.POST.get("caseIds", "")

        task = TestTask.objects.create(name=name, description=description, cases=case_ids)
        if task is None:
            return response_fail("创建失败！")
        return response_succeed("创建成功！")
    else:
        return response_fail("该接口只支持POST请求！")