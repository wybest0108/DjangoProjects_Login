from django.contrib.auth.decorators import login_required
from interface_app.models import TestCase, TestTask
from test_platform.common import response_succeed, response_fail
from interface_app.views.case_api import generate_ztree_nodes


@login_required
def save_task(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        if name == "":
            return response_fail("任务名称不能为空！")

        description = request.POST.get("description", "")
        case_ids = request.POST.get("caseIds", "")

        task = TestTask.objects.create(name=name, description=description, cases=case_ids)
        if task is None:
            return response_fail("创建失败！")
        return response_succeed("创建成功！")
    else:
        return response_fail("该接口只支持POST请求！")


@login_required
def get_task_info(request, task_id):
    if request.method == "GET":
        if task_id == "":
            return response_fail("任务ID为空！")

        try:
            task = TestTask.objects.get(id=task_id)
        except TestTask.DoesNotExist:
            return response_fail("任务ID不存在！")

        # 构造“已选用例树”节点数据
        ztree_nodes_selected_cases = [
            {
                "zId": 0,
                "name": "已选用例",
                "open": "true",
                "UID": "0_0_0"              # 使用"项目id_模块id_用例id"作为唯一标识
            }
        ]

        case_ids = []
        if task.cases != "":
            case_ids.extend(task.cases.split(","))
            cases_selected = []
            for case_id in case_ids:
                cases_selected.append(TestCase.objects.get(id=case_id))
            generate_ztree_nodes(ztree_nodes_selected_cases, cases_selected, case_ids)

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
        generate_ztree_nodes(ztree_nodes_all_cases, case_all, case_ids)

        return response_succeed(
            data={
                "name": task.name,
                "description": task.description,
                "ztreeNodesForAllCases": ztree_nodes_all_cases,
                "ztreeNodesForSelectedCases": ztree_nodes_selected_cases
            }
        )

    else:
        return response_fail("该接口只支持GET请求！")


@login_required
def update_task(request, task_id):
    if request.method == "POST":
        name = request.POST.get("name", "")
        if name == "":
            return response_fail("任务名称不能为空！")

        description = request.POST.get("description", "")
        case_ids = request.POST.get("caseIds", "")

        task = TestTask.objects.filter(id=task_id).update(name=name, description=description, cases=case_ids)

        if task == 1:
            return response_succeed("更新成功！")
        else:
            response_fail("更新失败！")
    else:
        return response_fail("该接口只支持POST请求！")
