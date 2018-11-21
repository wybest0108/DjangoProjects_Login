from django.urls import path
from interface_app.views import case_views, case_api

urlpatterns = [
    # 用例管理 urls
    path("case_manage/", case_views.case_manage),
    path("search_case/", case_views.search_case),
    path("add_case/", case_views.add_case),
    path("edit_case/<int:case_id>/", case_views.edit_case),
    path("delete_case/<int:case_id>/", case_views.delete_case),

    path("debug_case/", case_api.debug_case),
    path("get_projects_and_modules/", case_api.get_projects_and_modules),
    path("save_case/", case_api.save_case),
    path("get_case_info/<int:case_id>/", case_api.get_case_info),
    # path("delete_case/<int:case_id>/", case_views.delete_case),
    # path("edit_case/<int:case_id>/", case_views.edit_case),

]
