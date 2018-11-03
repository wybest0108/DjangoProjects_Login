from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.contrib.auth.models import User
from time import sleep


class LoginUITestCase(StaticLiveServerTestCase):
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

    # 测试用户名为空
    def test_username_empty(self):
        self.driver.get("%s%s" % (self.live_server_url, "/"))
        self.driver.find_element_by_name("username").send_keys("")
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(),'登录')]").click()
        error_tips = self.driver.find_elements_by_class_name("errorText")[0].text
        # error_tips = self.driver.find_element_by_tag_name("p").text
        self.assertEqual("用户名或者密码为空", error_tips)

    # 测试密码为空
    def test_password_empty(self):
        self.driver.get("%s%s" % (self.live_server_url, "/"))
        self.driver.find_element_by_name("username").send_keys("Linda01")
        self.driver.find_element_by_name("password").send_keys("")
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(),'登录')]").click()
        error_tips = self.driver.find_elements_by_class_name("errorText")[0].text
        self.assertEqual("用户名或者密码为空", error_tips)

    # 测试用户名或密码错误
    def test_username_password_error(self):
        self.driver.get("%s%s" % (self.live_server_url, "/"))
        self.driver.find_element_by_name("username").send_keys("Linda01")
        self.driver.find_element_by_name("password").send_keys("123")
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(),'登录')]").click()
        error_tips = self.driver.find_elements_by_class_name("errorText")[0].text
        self.assertEqual("用户名或者密码错误", error_tips)

        # 测试用户名或密码正确
    def test_username_password_correct(self):
        self.driver.get("%s%s" % (self.live_server_url, "/"))
        self.driver.find_element_by_name("username").send_keys("Linda01")
        self.driver.find_element_by_name("password").send_keys("Linda01123456")
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(),'登录')]").click()
        success_tips = self.driver.find_element_by_xpath("//div[@id='navbar']/ul/li[1]").text
        self.assertEqual("欢迎您，Linda01", success_tips)


