from django.http import JsonResponse


def response_succeed(message="请求成功", data={}):
    content = {
        "success": "true",
        "message": message,
        "data": data,
    }
    return JsonResponse(content)


def response_fail(message="参数错误"):
    content = {
        "success": "false",
        "message": message,
    }
    return JsonResponse(content)
