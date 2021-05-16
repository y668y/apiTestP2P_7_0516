import random
import unittest,logging,requests

from api.loginAPI import loginAPI

from api.trustAPI import trustAPI
from utils import assert_utils, third_request_api

from bs4 import BeautifulSoup


class Trust(unittest.TestCase):
    def setUp(self):
        self.login_api=loginAPI()
        self.trust_api=trustAPI()
        self.session=requests.Session()

    def tearDown(self):
        self.session.close()

    #发送开户请求
    def test01_trust_request(self):
        #1、认证通过的账号登录
        response=self.login_api.login(self.session)
        logging.info("login response={}".format(response.json))
        assert_utils(self,response,200,200,"登录成功")
        #2、发送开户请求
        response=self.trust_api.trust_register(self.session)
        logging.info("trust response={}".format(response.json))
        self.assertEqual(200,response.status_code)
        self.assertEqual(200,response.json().get("status"))
        #3、发送第三方开户请求
        form_data=response.json().get("description").get("form")
        logging.info("form response={}".format(form_data))
        #调用第三方接口的请求方法
        response=third_request_api(form_data)
        # 断言响应结果
        self.assertEqual(200, response.status_code)
        self.assertEqual("UserRegister OK", response.text)

    #充值成功
    def recharge(self):
        #1、登录成功
        response = self.login_api.login(self.session)
        logging.info("login response={}".format(response.json))
        assert_utils(self, response, 200, 200, "登录成功")
        #2、发送充值验证码
        r=random()
        response=self.trust_api.get_recharge_verify_code(self.session,str(r))
        logging.info("get recharge verify code response={}".format(response.text))
        self.assertEqual(200,response.status_code)
        #3、发送充值请求
        response = self.trust_api.recharge(self.session,"10000")
        logging.info("recharge response={}".format(response.json))
        self.assertEqual(200,response.status_code)
        self.assertEqual(200,response.json().get("status"))
        #4、发送第三方充值请求
        form_data = response.json().get("description").get("form")
        logging.info("third recharge request response={}".format(form_data))
        # 调用第三方接口的请求方法
        response = third_request_api(form_data)
        # 断言响应结果
        self.assertEqual(200, response.status_code)
        self.assertEqual("NetSave OK", response.text)





