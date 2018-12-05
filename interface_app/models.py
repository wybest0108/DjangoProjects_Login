from django.db import models
from project_app.models import Module


class TestCase(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, verbose_name="模块")
    name = models.CharField("名称", max_length=100, default="", blank=False, null=False)
    url = models.TextField("URL", default="", blank=False, null=False)
    request_method = models.CharField("方法", max_length=10, default="GET", blank=False, null=False)
    request_headers = models.TextField("Headers", default="", blank=True, null=True)
    request_params_type = models.CharField("参数类型", max_length=10, default="form-data", blank=False, null=False)
    request_params = models.TextField("参数", default="", blank=True, null=True)
    response_assert = models.TextField("验证", default="", blank=True, null=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.name


class TestTask(models.Model):
    name = models.CharField("名称", max_length=100, default="", blank=False, null=False)
    description = models.TextField("描述", default="", blank=True, null=True)
    status = models.IntegerField("状态", default=0)
    cases = models.TextField("关联用例", default="", blank=True, null=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.name
