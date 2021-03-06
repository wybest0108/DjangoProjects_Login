from django.db import models


class Project(models.Model):
    name = models.CharField("名称", max_length=100, default="", blank=False, null=False)
    description = models.TextField("描述", default="", blank=True, null=True)
    status = models.BooleanField("状态", default=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.name


class Module(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="项目")
    name = models.CharField("名称", max_length=100, default="", blank=False, null=False)
    description = models.TextField("描述", default="", blank=True, null=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.name
