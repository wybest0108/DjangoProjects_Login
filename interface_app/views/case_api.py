from django.contrib.auth.decorators import login_required
from interface_app.models import TestCase
from project_app.models import Project, Module
from test_platform.common import response_succeed, response_fail
import requests
import json


@login_required
def debug_case(request):
    if request.method == "POST":
        url = request.POST.get("url", "")
        method = request.POST.get("method", "").upper()
        param_type = request.POST.get("paramType", "").upper()
        try:
            headers = json.loads(request.POST.get("headers", "{}").replace("'", "\""))
            params = json.loads(request.POST.get("params", "{}").replace("'", "\""))
        except json.decoder.JSONDecodeError:
            return response_fail("Header或参数格式不符合要求！")

        if url == "" or method == "" or param_type == "":
            return response_fail("URL、请求方法、请求参数类型不能为空！")

        if method == "GET":
            if param_type == "FORM-DATA":
                r = requests.get(url, params=params, headers=headers)
            else:
                return response_fail("请求参数类型错误！")

        if method == "POST":
            if param_type == "FORM-DATA":
                r = requests.post(url, data=params, headers=headers)
            elif param_type == "JSON":
                r = requests.post(url, json=params, headers=headers)
            else:
                return response_fail("请求参数类型错误！")

        return response_succeed(data=r.text)
    else:
        return response_fail("该接口只支持POST请求！")


@login_required
def get_projects_and_modules(request):
    if request.method == "GET":
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

        return response_succeed(data={"projects": project_list})
    else:
        return response_fail("该接口只支持GET请求！")


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
        assert_text = request.POST.get("assertText", "")

        if module_name == "" or name == "" or url == "" or method == "" or param_type == "":
            return response_fail("模块名、用例名、url、请求方法、请求参数类型不能为空！")

        case = TestCase.objects.create(
            module=Module.objects.get(name=module_name),
            name=name,
            url=url,
            request_method=method,
            request_headers=headers,
            request_params_type=param_type,
            request_params=params,
            response_assert=assert_text,
        )

        if case is not None:
            return response_succeed("保存成功！")
        else:
            return response_fail("未知错误！保存失败！")

    else:
        return response_fail("该接口只支持POST请求！")


@login_required
def get_case_info(request, case_id):
    if case_id:
        target_case = TestCase.objects.get(id=case_id)
        response_data = {}
        response_data["name"] = target_case.name
        response_data["url"] = target_case.url
        response_data["method"] = target_case.request_method
        response_data["headers"] = target_case.request_headers
        response_data["paramsType"] = target_case.request_params_type
        response_data["params"] = target_case.request_params
        response_data["assertText"] = target_case.response_assert
        module = target_case.module
        response_data["moduleName"] = module.name
        response_data["projectName"] = module.project.name
        return response_succeed(data=response_data)
    else:
        return response_fail("用例ID不存在！")


@login_required
def update_case(request, case_id):
    if request.method == "POST":
        module_name = request.POST.get("moduleName", "")
        name = request.POST.get("name", "")
        url = request.POST.get("url", "")
        method = request.POST.get("method", "").upper()
        param_type = request.POST.get("paramType", "")
        headers = request.POST.get("headers", "{}")
        params = request.POST.get("params", "{}")
        assert_text = request.POST.get("assertText", "")

        if module_name == "" or name == "" or url == "" or method == "" or param_type == "":
            return response_fail("模块名、用例名、url、请求方法、请求参数类型不能为空！")

        case = TestCase.objects.filter(id=case_id).update(
            module=Module.objects.get(name=module_name),
            name=name,
            url=url,
            request_method=method,
            request_headers=headers,
            request_params_type=param_type,
            request_params=params,
            response_assert=assert_text,
        )

        if case == 1:
            return response_succeed("更新成功！")
        else:
            response_fail("更新失败！")
    else:
        return response_fail("该接口只支持POST请求！")


@login_required
def assert_result(request):
    if request.method == "POST":
        response_result = request.POST.get("response_result", "")
        assert_text = request.POST.get("assert_text", "")

        if response_result == "" or assert_text == "":
            return response_fail("验证数据或者响应结果不能为空！")

        try:
            assert assert_text in response_result
        except AssertionError:
            return response_fail("验证失败！")
        else:
            return response_succeed("验证成功！")
    else:
        return response_fail("该接口只支持POST请求！")


@login_required
def get_cases_for_ztree(request):
    if request.method == "GET":

        # 构造“已选用例树”节点数据
        ztree_nodes_selected_cases = [
            {
                "zId": 0,
                "name": "已选用例",
                "open": "true",
                "UID": "0_0_0"                  # 使用"项目id_模块id_用例id"作为唯一标识
            }
        ]

        # 构造“可选用例树”节点数据
        ztree_nodes_all_cases = [
            {
                "zId": 0,
                "name": "可选用例",
                "open": "true",
                "UID": "0_0_0"
            }
        ]
        case_all = TestCase.objects.all()
        generate_ztree_nodes(ztree_nodes_all_cases, case_all)

        return response_succeed(
            data={
                "ztreeNodesForAllCases": ztree_nodes_all_cases,
                "ztreeNodesForSelectedCases": ztree_nodes_selected_cases
            }
        )
    else:
        return response_fail("该接口只支持GET请求！")


# 构造zTree节点数据
def generate_ztree_nodes(ztree_nodes, cases, checked_cases=[]):
    num = 0
    project_dict = {}
    module_dict = {}

    for case in cases:
        if str(case.id) in checked_cases:
            is_checked = "true"
        else:
            is_checked = "false"

        project = case.module.project
        if project.name not in project_dict:
            num += 1
            pid = num
            znode = {}
            znode["zId"] = num
            znode["pId"] = 0
            znode["name"] = project.name
            znode["UID"] = str(project.id) + "_0_0"
            ztree_nodes.append(znode)
            project_dict[project.name] = pid
        else:
            pid = project_dict[project.name]

        module = case.module
        if module.name not in module_dict:
            num += 1
            pid_1 = num
            znode_1 = {}
            znode_1["zId"] = num
            znode_1["pId"] = pid
            znode_1["name"] = module.name
            znode_1["UID"] = str(project.id) + "_" + str(module.id) + "_0"
            ztree_nodes.append(znode_1)
            module_dict[module.name] = pid_1
        else:
            pid_1 = module_dict[module.name]

        num += 1
        znode_2 = {}
        znode_2["zId"] = num
        znode_2["pId"] = pid_1
        znode_2["name"] = case.name
        znode_2["caseId"] = case.id
        znode_2["checked"] = is_checked
        znode_2["UID"] = str(project.id) + "_" + str(module.id) + "_" + str(case.id)
        ztree_nodes.append(znode_2)
