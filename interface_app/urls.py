from django.urls import path
from interface_app import views

urlpatterns = [
    # 用例管理 urls
    path("case_manage/", views.case_manage),
    path("api_debug/", views.api_debug),
]
