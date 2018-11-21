from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from interface_app.models import TestCase


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
def add_case(request):
    if request.method == "GET":
        return render(request, "test_case.html", {
            "type": "add"
        })
    else:
        return HttpResponse("404")


@login_required
def edit_case(request, case_id):
    print(case_id)
    if request.method == "GET":
        return render(request, "test_case.html", {
            "type": "edit"
        })
    else:
        return HttpResponse("404")


@login_required
def delete_case(request, case_id):
    TestCase.objects.get(id=case_id).delete()
    return HttpResponseRedirect("/interface/case_manage/")
