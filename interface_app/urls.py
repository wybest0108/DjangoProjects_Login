from django.urls import path
from interface_app import case_views

urlpatterns = [
    # 用例管理 urls
    path("case_manage/", case_views.case_manage),
    path("search_case/", case_views.search_case),
    path("debug_case/", case_views.debug_case),
    path("save_case/", case_views.save_case),
    path("get_projects_and_modules/", case_views.get_projects_and_modules),
    path("delete_case/<int:case_id>/", case_views.delete_case),
]
