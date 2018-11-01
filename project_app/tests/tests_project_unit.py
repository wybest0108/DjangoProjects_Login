from django.test import TestCase
from project_app.models import Project
from django.contrib.auth.models import User
from django.test import Client


# 项目管理单元测试
class ProjectTestCase(TestCase):
    def setUp(self):
        User.objects.create_user("Linda01", "Linda01@gmail.com", "Linda01123456")
        Project.objects.create(name="项目Test1", description="描述Test1")
        Project.objects.create(name="项目Test2", description="描述Test2")
        self.client = Client()
        self.client.post("/login_action/", {"username": "Linda01", "password": "Linda01123456"})

    # 测试项目列表
    def test_project_manage(self):
        response = self.client.get("/manage/project_manage/")
        response_content_html = response.content.decode("utf-8")
        self.assertEquals(response.status_code, 200)
        self.assertIn("项目Test1", response_content_html)

    # 测试项目查询
    def test_search_project(self):
        # 查询关键字不为空
        response = self.client.get("/manage/search_project/", {"keyword": "Test2"})
        response_content_html = response.content.decode("utf-8")
        self.assertEquals(response.status_code, 200)
        self.assertIn("项目Test2", response_content_html)
        self.assertNotIn("项目Test1", response_content_html)
        # 查询关键字为空
        response = self.client.get("/manage/search_project/", {"keyword": ""})
        self.assertRedirects(response, "/manage/project_manage/")

    # 测试新增项目
    def test_add_project(self):
        response = self.client.post("/manage/add_project/", {"name": "项目Test3", "description": "描述Test3"})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(len(Project.objects.filter(name__contains="项目Test3")), 1)

    # 测试删除项目
    def test_delete_project(self):
        response = self.client.get("/manage/delete_project/1/")
        self.assertEquals(response.status_code, 302)
        self.assertEquals(len(Project.objects.filter(name__contains="项目Test1")), 0)

    # 测试编辑项目（get请求，用于获取json数据并返回给前端页面)
    def test_edit_project(self):
        response = self.client.get("/manage/edit_project/1/")
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(response.content, '{"name": "项目Test1", "description": "描述Test1", "status": true}')

    # 测试编辑项目（post请求，用于更新数据）
    def test_edit_project_save(self):
        response = self.client.post("/manage/edit_project_save/1/", {"name": "项目Test1", "description": "项目Test1的描述已经被更新"})
        project = Project.objects.get(name="项目Test1")
        self.assertEquals(response.status_code, 302)
        self.assertEquals(project.description, "项目Test1的描述已经被更新")
