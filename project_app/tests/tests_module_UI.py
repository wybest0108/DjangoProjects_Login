from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.select import Select
from django.contrib.auth.models import User
from project_app.models import Project, Module
from time import sleep


class ModuleUITestCase(StaticLiveServerTestCase):
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
        project = Project.objects.get(name="项目Test1")
        Module.objects.create(project=project, name="模块Test1", description="这里是模块Test1的描述")
        Module.objects.create(project=project, name="模块Test2", description="这里是模块Test2的描述")
        self.driver.get("%s%s" % (self.live_server_url, "/"))
        self.driver.find_element_by_name("username").send_keys("Linda01")
        self.driver.find_element_by_name("password").send_keys("Linda01123456")
        self.driver.find_element_by_xpath("//button[contains(text(),'登录')]").click()
        self.driver.find_element_by_link_text("模块管理").click()
        sleep(1)

    # 测试模块列表
    def test_module_manage(self):
        module_name = self.driver.find_element_by_xpath("//tbody/tr/td[1]").text
        sleep(2)
        self.assertEqual("模块Test1", module_name)

    # 测试模块查询
    def test_search_module(self):
        # 查询关键字不为空
        self.driver.find_element_by_name("keyword").send_keys("Test1")
        self.driver.find_element_by_xpath("//input[@value='搜索']").click()
        sleep(2)
        search_result = self.driver.page_source
        self.assertIn("模块Test1", search_result)
        self.assertNotIn("模块Test2", search_result)
        # 查询关键字为空
        self.driver.find_element_by_name("keyword").send_keys("")
        self.driver.find_element_by_xpath("//input[@value='搜索']").click()
        sleep(2)
        search_result = self.driver.page_source
        self.assertIn("模块Test1", search_result)
        self.assertIn("模块Test2", search_result)

    # 测试新增模块
    def test_add_module(self):
        self.driver.find_element_by_xpath("//button[contains(text(),'新增')]").click()
        self.assertIn("新增模块", self.driver.page_source)
        Select(self.driver.find_element_by_id("id_project")).select_by_value("1")
        self.driver.find_element_by_id("id_name").send_keys("模块Test3")
        self.driver.find_element_by_id("id_description").send_keys("模块Test3的描述")
        sleep(1)
        self.driver.find_element_by_xpath("//button[contains(text(),'创建')]").click()
        self.assertIn("模块Test3", self.driver.page_source)
        self.assertIn("模块Test3的描述", self.driver.page_source)

    # 测试删除模块
    def test_delete_module(self):
        self.driver.find_element_by_xpath("//tbody/tr[1]/td[5]/a[2]").click()
        sleep(1)
        self.assertIn("确认删除", self.driver.page_source)
        self.driver.find_element_by_xpath("//button[contains(text(),'确定')]").click()
        self.assertNotIn("模块Test1", self.driver.page_source)

    # 测试编辑模块
    def test_edit_module(self):
        self.driver.find_element_by_xpath("//tbody/tr[1]/td[5]/a[1]").click()
        self.assertIn("编辑模块", self.driver.page_source)
        # 依次修改模块所属项目、名称和描述
        Select(self.driver.find_element_by_id("id_project")).select_by_value("2")
        name_input = self.driver.find_element_by_id("id_name")
        name_input.clear()
        name_input.send_keys("模块Test1名称被更新")
        description_input = self.driver.find_element_by_id("id_description")
        description_input.clear()
        description_input.send_keys("模块Test1的描述已经被更新")
        sleep(1)
        self.driver.find_element_by_xpath("//button[contains(text(),'保存')]").click()
        # 检查名称、描述和状态是否与修改的值一致
        self.assertIn("模块Test1名称被更新", self.driver.page_source)
        self.assertIn("模块Test1的描述已经被更新", self.driver.page_source)
        project_name = self.driver.find_element_by_xpath("//td[contains(text(),'模块Test1名称被更新')]//../td[2]").text
        self.assertEqual("项目Test2", project_name)





