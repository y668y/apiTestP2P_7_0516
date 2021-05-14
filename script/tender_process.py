import logging
import random
import unittest

import requests

import app
from utils import DButils

from api.loginAPI import loginAPI
from api.tenderAPI import tenderAPI
from api.trustAPI import trustAPI



        # 充值
        # 投标：查看投标详情页、投资、投资第三方接口、查看投资列表
from utils import assert_utils, third_request_api


class test_tender_process(unittest.TestCase):
    phone1 = "13033446623"
    tender_id = "448"
    pwd="1111aaaa"
    imgCode = "8888"

    @classmethod
    def setUpClass(cls):
        cls.login_api = loginAPI()
        cls.tender_api = tenderAPI()
        cls.session = requests.Session()
        cls.trust_api=trustAPI()

    @classmethod
    def tearDownClass(cls):
        cls.session.close()
        sql1="delete from mb_member_register_log where phone in ('13033446623');"
        DButils.delete(app.DB_MEMBER,sql1)
        logging.info("delete sql={}".format(sql1))
        sql2="delete i.* from mb_member_login_log i INNER JOIN mb_member m on i.member_id = m.id WHERE m.phone in ('13033446623');"
        DButils.delete(app.DB_MEMBER, sql2)
        logging.info("delete sql={}".format(sql2))
        sql3="delete i.* from mb_member_info i INNER JOIN mb_member m on i.member_id = m.id WHERE m.phone in ('13099981123');"
        DButils.delete(app.DB_MEMBER, sql3)
        logging.info("delete sql={}".format(sql3))
        sql4="delete from mb_member WHERE phone in ('13033446623');"
        DButils.delete(app.DB_MEMBER, sql4)
        logging.info("delete sql={}".format(sql4))



    # 输入必填项-注册成功
    def test01_register_success_input_mandatory(self):
        # 1、获取图片验证码
        # 定义参数
        r = random.randint(10000000, 90000000)
        # 调用接口类中的接口请求
        response = self.login_api.getImgCode(self.session, str(r))
        print(response.status_code)
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)
        # 2、获取短信验证码
        # 定义参数
        # 调用接口类中的接口请求
        response = self.login_api.getSmsCode(self.phone1, self.imgCode, self.session)
        logging.info("--------------------------------get sms code response={}".format(response.json()))
        # 接收接口返回的结果，进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")
        #3、注册成功
        # 定义参数
        # 调用接口类中的接口请求
        response = self.login_api.register(self.session,self.phone1,self.pwd)
        logging.info("--------------------------------get register response={}".format(response.json()))
        # 接收接口返回的结果，进行断言
        assert_utils(self, response, 200, 200, "注册成功")

    #登录成功
    def test02_login_success(self):
        #定义参数
        #调用接口类中的接口
        response=self.login_api.login(self.session,keywords=self.phone1,password=self.pwd)
        logging.info("--------------------------------get login response={}".format(response.json()))
        #接收接口返回的结果，并进行断言
        assert_utils(self,response,200,200,"登录成功")

    # 激活：开通账号、发送第三方接口开户
    def test03_trust_request(self):
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
    def test04_recharge(self):
        #1、登录成功
        response = self.login_api.login(self.session)
        logging.info("login response={}".format(response.json))
        assert_utils(self, response, 200, 200, "登录成功")
        #2、发送充值验证码
        r=random.random()
        response=self.trust_api.get_recharge_verify_code(self.session,str(r))
        logging.info("get recharge verify code response={}".format(response.text))
        self.assertEqual(200,response.status_code)
        #3、发送充值请求
        response = self.trust_api.recharge(self.session,"100000000")
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

    def test05_get_loaninfo(self):
        response=self.tender_api.get_loaninfo(self.session,self.tender_id)
        logging.info("get loaninfo response={}".format(response.json()))
        assert_utils(self,response,200,200,"OK")

    def test06_tender(self):
        response=self.tender_api.tender(self.session,self.tender_id,"100")
        logging.info("tender response={}".format(response.json()))
        self.assertEqual(200,response.status_code)
        self.assertEqual(200,response.json().get("status"))
        # 发送第三方请求
        form_data = response.json().get("description").get("form")
        logging.info("third tender request response={}".format(form_data))
        # 调用第三方接口的请求方法
        response = third_request_api(form_data)
        # 断言响应结果
        self.assertEqual(200, response.status_code)
        self.assertEqual("InitiativeTender OK", response.text)

    def test07_tenderlist(self):
        status="tender"
        response = self.tender_api.get_tenderlist(self.session,status)
        logging.info("get tenderlist response={}".format(response.json()))
        self.assertEqual(200, response.status_code)


