from django.contrib import admin
from interface_app.models import TestCase, TestTask


class TestCaseAdmin(admin.ModelAdmin):
    list_display = ["module", "name", "url", "request_method", "request_headers", "request_params_type", "request_params", "response_assert", "create_time"]


class TestTaskAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "status", "cases", "create_time"]


admin.site.register(TestCase, TestCaseAdmin)
admin.site.register(TestTask, TestTaskAdmin)