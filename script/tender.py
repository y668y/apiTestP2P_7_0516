import unittest,logging

import requests

from api.loginAPI import loginAPI
from api.trustAPI import trustAPI
from api.tenderAPI import tenderAPI
from utils import assert_utils, third_request_api


class tender(unittest.TestCase):
    def setUp(self):
        self.login_api=loginAPI()
        self.tender_api=tenderAPI()
        self.session=requests.Session()
        self.tender_id="448"
        self.phone="13111111113"
        self.pwd="1234qwer"


        response=self.login_api.login(self.session,self.phone,self.pwd)
        logging.info("login response={}".format(response.json()))
        assert_utils(self,response,200,200,"登录成功")

    def tearDown(self):
        self.session.close()

    def test01_get_loaninfo(self):
        response=self.tender_api.get_loaninfo(self.session,self.tender_id)
        logging.info("get loaninfo response={}".format(response.json()))
        assert_utils(self,response,200,200,"OK")

    def test02_tender(self):
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

    def test03_tenderlist(self):
        status="tender"
        response = self.tender_api.get_tenderlist(self.session,status)
        logging.info("get tenderlist response={}".format(response.json()))
        self.assertEqual(200, response.status_code)

