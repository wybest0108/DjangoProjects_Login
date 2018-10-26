from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client

# 测试User Model
class UserModelTestCase(TestCase):
    def setUp(self):
        # User.objects.create(username="Linda01", email="Linda01@gmail.com", password="Linda01123456")
        User.objects.create_user("Linda01", "Linda01@gmail.com", "Linda01123456")

    # 测试查询
    def test_User_select(self):
        result = User.objects.get(username="Linda01")
        self.assertEqual(result.email, "Linda01@gmail.com")

    # 测试新增
    def test_User_create(self):
        User.objects.create_user("Linda02", "Linda02@gmail.com", "Linda02123456")
        new_user = User.objects.get(username="Linda02")
        self.assertEqual(new_user.email, "Linda02@gmail.com")

    # 测试更新
    def test_User_update(self):
        User.objects.select_for_update().filter(username="Linda01").update(username="Linda0101", email="Linda0101@gmail.com")
        user = User.objects.get(username="Linda0101")
        self.assertEqual(user.email, "Linda0101@gmail.com")

    # 测试删除
    def test_User_delete(self):
        User.objects.get(username="Linda01").delete()
        users = User.objects.all()
        self.assertEqual(len(users), 0)


# 测试登录
class LoginTestCase(TestCase):
    def setUp(self):
        User.objects.create_user("Linda01", "Linda01@gmail.com", "Linda01123456")
        self.client = Client()

    # 测试打开登录首页
    def test_login_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    # 测试用户名为空
    def test_username_empty(self):
        response = self.client.post("/login_action/", {"username": ""})
        response_content_html = response.content.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertIn("用户名或者密码为空", response_content_html)

    # 测试密码为空
    def test_password_empty(self):
        response = self.client.post("/login_action/", {"username": "Linda01", "password": ""})
        response_content_html = response.content.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertIn("用户名或者密码为空", response_content_html)

    # 测试用户名或密码错误
    def test_username_password_error(self):
        response = self.client.post("/login_action/", {"username": "Linda", "password": "123"})
        response_content_html = response.content.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertIn("用户名或者密码错误", response_content_html)

    # 测试用户名或密码正确
    def test_username_password_correct(self):
        response = self.client.post("/login_action/", {"username": "Linda01", "password": "Linda01123456"})
        self.assertRedirects(response, "/manage/project_manage/")