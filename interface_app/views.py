from django.shortcuts import render
from django.http import HttpResponse
import requests
import json


def case_manage(request):
    if request.method == "GET":
        return render(request, "case_manage.html", {
            "type": "list"
        })
    else:
        return HttpResponse("404")


def api_debug(request):
    if request.method == "POST":
        name = request.POST.get("name")
        url = request.POST.get("url")
        method = request.POST.get("method")
        paramType = request.POST.get("paramType")
        headers = json.loads(request.POST.get("headers").replace("'", "\""))
        params = json.loads(request.POST.get("params").replace("'", "\""))
        if method == "get":
            r = requests.get(url, params=params, headers=headers)

        if method == "post":
            if paramType == "form-data":
                print("form-data")
                r = requests.post(url, data=params, headers=headers)
            if paramType == "json":
                print("json")
                r = requests.post(url, json=params, headers=headers)

        return HttpResponse(r.text)
    else:
        return render(request, "api_debug.html", {
            "type": "debug"
        })
