from django.urls import path
from interface_app.views import case_views, case_api, task_views, task_api

urlpatterns = [
    # 用例管理之视图urls
    path("case_manage/", case_views.case_manage),
    path("search_case/", case_views.search_case),
    path("add_case/", case_views.add_case),
    path("edit_case/<int:case_id>/", case_views.edit_case),
    path("delete_case/<int:case_id>/", case_views.delete_case),
    # 用例管理之接口urls
    path("debug_case/", case_api.debug_case),
    path("get_projects_and_modules/", case_api.get_projects_and_modules),
    path("save_case/", case_api.save_case),
    path("get_case_info/<int:case_id>/", case_api.get_case_info),
    path("assert_result/", case_api.assert_result),
    path("update_case/<int:case_id>/", case_api.update_case),
    path("get_cases_for_ztree/", case_api.get_cases_for_ztree),

    # 任务管理之视图urls
    path("task_manage/", task_views.task_manage),
    path("search_task/", task_views.search_task),
    path("add_task/", task_views.add_task),
    path("delete_task/<int:task_id>/", task_views.delete_task),
    # 任务管理之接口urls
    path("save_task/", task_api.save_task),
]
