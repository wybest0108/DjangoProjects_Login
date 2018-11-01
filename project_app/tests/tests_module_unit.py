from django.test import TestCase
from project_app.models import Project, Module
from django.contrib.auth.models import User
from django.test import Client


# 模块管理单元测试
class ModuleTestCase(TestCase):
    def setUp(self):
        User.objects.create_user("Linda01", "Linda01@gmail.com", "Linda01123456")
        Project.objects.create(name="项目Test1", description="描述Test1")
        project = Project.objects.get(name="项目Test1")
        Module.objects.create(project=project, name="模块Test1", description="这里是模块Test1的描述")
        self.client = Client()
        self.client.post("/login_action/", {"username": "Linda01", "password": "Linda01123456"})

    # 测试模块列表
    def test_module_manage(self):
        response = self.client.get("/manage/module_manage/")
        response_content_html = response.content.decode("utf-8")
        self.assertEquals(response.status_code, 200)
        self.assertIn("模块Test1", response_content_html)

    # 测试模块查询
    def test_search_module(self):
        # 查询关键字不为空
        response = self.client.get("/manage/search_module/", {"keyword": "Test1"})
        self.assertEquals(response.status_code, 200)
        self.assertIn("模块Test1", response.content.decode("utf-8"))
        # 查询关键字为空
        response = self.client.get("/manage/search_module/", {"keyword": ""})
        self.assertRedirects(response, "/manage/module_manage/")

    # 测试新增模块
    def test_add_project(self):
        # 测试get请求
        response = self.client.get("/manage/add_module/")
        self.assertEquals(response.status_code, 200)
        self.assertIn("新增模块", response.content.decode("utf-8"))
        # 测试post请求(有效参数）
        response = self.client.post("/manage/add_module/", {"name": "模块Test2", "description": "模块Test2的描述", "project": 1})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(len(Module.objects.filter(name__contains="模块Test2")), 1)
        # 测试post请求(无效参数）
        self.client.post("/manage/add_module/", {"name": "", "description": "", "project": 1})
        self.assertEquals(len(Module.objects.all()), 2)

    # 测试删除模块
    def test_delete_module(self):
        response = self.client.get("/manage/delete_module/1/")
        self.assertEquals(response.status_code, 302)
        self.assertEquals(len(Module.objects.filter(name__contains="模块Test1")), 0)

    # 测试编辑模块
    def test_edit_project(self):
        # 测试get请求
        response = self.client.get("/manage/edit_module/1/")
        self.assertEquals(response.status_code, 200)
        self.assertIn("模块Test1", response.content.decode("utf-8"))
        # 测试post请求
        response = self.client.post("/manage/edit_module/1/", {"name": "模块Test2(修改后）", "description": "模块Test2的描述(修改后)", "project": 1})
        self.assertEquals(response.status_code, 302)
        module = Module.objects.get(name="模块Test2(修改后）")
        self.assertEquals(module.description, "模块Test2的描述(修改后)")

