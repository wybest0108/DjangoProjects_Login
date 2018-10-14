from django.urls import path, re_path
from project_app import views

urlpatterns = [
    path("project_manage/", views.project_manage),
    path("module_manage/", views.module_manage),
    path("search_project/", views.search_project),
    path("add_project/", views.add_project),
    path("add_project/", views.add_project),
    re_path(r"^delete_project/(?P<project_id>[0-9]+)/$", views.delete_project),
    re_path(r"^edit_project/(?P<project_id>[0-9]+)/$", views.edit_project),
    re_path(r"^edit_project_save/(?P<project_id>[0-9]+)/$", views.edit_project_save),
]