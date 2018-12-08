from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from interface_app.models import TestTask


@login_required()
def task_manage(request):
    if request.method == "GET":
        task_all = TestTask.objects.all()

        paginator = Paginator(task_all, 3)
        page = request.GET.get("page")
        try:
            tasks = paginator.page(page)
        except PageNotAnInteger:
            tasks = paginator.page(1)
        except EmptyPage:
            tasks = paginator.page(paginator.num_pages)

        return render(request, "task_manage.html", {
            "tasks": tasks,
            "type": "list"
        })

    else:
        return HttpResponse("404")


@login_required
def search_task(request):
    if request.method == "GET":
        keyword = request.GET.get("keyword", "")
        result_list = TestTask.objects.filter(name__contains=keyword)

        paginator = Paginator(result_list, 3)
        page = request.GET.get("page")
        try:
            tasks = paginator.page(page)
        except PageNotAnInteger:
            tasks = paginator.page(1)
        except EmptyPage:
            tasks = paginator.page(paginator.num_pages)

        return render(request, "task_manage.html", {
            "tasks": tasks,
            "type": "list",
            "keyword": keyword,
        })
    else:
        return HttpResponse("404")


@login_required
def add_task(request):
    if request.method == "GET":
        return render(request, "test_task.html", {
            "type": "add"
        })
    else:
        return HttpResponse("404")


@login_required
def edit_task(request, task_id):
    if request.method == "GET":
        return render(request, "test_task.html", {
            "type": "edit"
        })
    else:
        return HttpResponse("404")


@login_required
def delete_task(request, task_id):
    TestTask.objects.get(id=task_id).delete()
    return HttpResponseRedirect("/interface/task_manage/")
