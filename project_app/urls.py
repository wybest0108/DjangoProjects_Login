from django.urls import path
from project_app.views import project_views, module_views

urlpatterns = [
    # 项目 urls
    path("project_manage/", project_views.project_manage),
    path("search_project/", project_views.search_project),
    path("add_project/", project_views.add_project),
    path("delete_project/<int:project_id>/", project_views.delete_project),
    path("edit_project/<int:project_id>/", project_views.edit_project),
    path("edit_project_save/<int:project_id>/", project_views.edit_project_save),
    # re_path(r"^delete_project/(?P<project_id>[0-9]+)/$", project_views.delete_project),
    # re_path(r"^edit_project/(?P<project_id>[0-9]+)/$", project_views.edit_project),
    # re_path(r"^edit_project_save/(?P<project_id>[0-9]+)/$", project_views.edit_project_save),

    # 模块 urls
    path("module_manage/", module_views.module_manage),
    path("search_module/", module_views.search_module),
    path("add_module/", module_views.add_module),
    path("edit_module/<int:mid>/", module_views.edit_module),
    path("delete_module/<int:mid>/", module_views.delete_module),
]
