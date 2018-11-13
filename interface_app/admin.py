from django.contrib import admin
from interface_app.models import TestCase


class TestCaseAdmin(admin.ModelAdmin):
    list_display = ["name", "url", "request_method", "request_headers", "request_params_type", "request_params", "response_assert", "create_time"]


admin.site.register(TestCase, TestCaseAdmin)

