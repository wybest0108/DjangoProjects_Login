from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.contrib.auth.models import User
from project_app.models import Project
from time import sleep


class ProjectUITestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Firefox()
        # cls.driver.implicity_wait(10)
        # cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        User.objects.create_user("Linda01", "Linda01@gmail.com", "Linda01123456")
        Project.objects.create(name="项目Test1", description="描述Test1")
        Project.objects.create(name="项目Test2", description="描述Test2")
        self.driver.get("%s%s" % (self.live_server_url, "/"))
        self.driver.find_element_by_name("username").send_keys("Linda01")
        self.driver.find_element_by_name("password").send_keys("Linda01123456")
        self.driver.find_element_by_xpath("//button[contains(text(),'登录')]").click()

    # 测试项目列表
    def test_project_manage(self):
        first_project_name = self.driver.find_element_by_xpath("//tbody/tr/td[1]").text
        sleep(2)
        self.assertEqual("项目Test1", first_project_name)

    # 测试项目查询
    def test_search_project(self):
        # 查询关键字不为空
        self.driver.find_element_by_name("keyword").send_keys("Test1")
        self.driver.find_element_by_xpath("//input[@value='搜索']").click()
        sleep(2)
        search_result = self.driver.page_source
        self.assertIn("项目Test1", search_result)
        self.assertNotIn("项目Test2", search_result)
        # 查询关键字为空
        self.driver.find_element_by_name("keyword").send_keys("")
        self.driver.find_element_by_xpath("//input[@value='搜索']").click()
        sleep(2)
        search_result = self.driver.page_source
        self.assertIn("项目Test1", search_result)
        self.assertIn("项目Test2", search_result)

    # 测试新增项目
    def test_add_project(self):
        self.driver.find_element_by_xpath("//button[contains(text(),'新增')]").click()
        self.assertIn("新建项目", self.driver.page_source)
        self.driver.find_element_by_xpath("//input[@id='name']").send_keys("项目Test3")
        self.driver.find_element_by_xpath("//textarea[@id='description']").send_keys("项目Test3的描述")
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(),'提交')]").click()
        self.assertIn("项目Test3", self.driver.page_source)
        self.assertIn("项目Test3的描述", self.driver.page_source)

    # 测试删除项目
    def test_delete_project(self):
        self.driver.find_element_by_xpath("//tbody/tr[1]/td[5]/a[2]").click()
        sleep(1)
        self.assertIn("确认删除", self.driver.page_source)
        self.driver.find_element_by_xpath("//button[contains(text(),'确定')]").click()
        self.assertNotIn("项目Test1", self.driver.page_source)

    # 测试编辑项目
    def test_edit_project(self):
        self.driver.find_element_by_xpath("//tbody/tr[1]/td[5]/a[1]").click()
        self.assertIn("编辑项目", self.driver.page_source)
        # 依次修改项目名称、描述和状态
        name_input = self.driver.find_element_by_xpath("//label[contains(text(),'名称')]/../../td[2]/input")
        name_input.clear()
        name_input.send_keys("项目Test1名称被更新")
        description_input = self.driver.find_element_by_xpath("//textarea")
        description_input.clear()
        description_input.send_keys("描述Test1已经被更新")
        status_input = self.driver.find_element_by_xpath("//input[@type='checkbox']")
        status_input.click()
        sleep(1)
        self.driver.find_element_by_xpath("//button[contains(text(),'保存')]").click()
        # 检查名称、描述和状态是否与修改的值一致
        self.assertIn("项目Test1名称被更新", self.driver.page_source)
        self.assertIn("描述Test1已经被更新", self.driver.page_source)
        status = self.driver.find_element_by_xpath("//td[contains(text(),'项目Test1名称被更新')]//../td[3]/img").get_attribute("alt")
        self.assertEqual("False", status)





