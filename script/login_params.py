import logging
import random
import time
import unittest
from parameterized import parameterized

import requests

from api.loginAPI import loginAPI
from utils import assert_utils, read_imgverify_data, read_register_data, read_param_data


class Login(unittest.TestCase):


    def setUp(self):
        self.login_api=loginAPI()
        self.session=requests.Session()
        self.phone1 = "13033446614"
        self.phone2 = "13033446615"
        self.phone3="13033446616"
        self.phone4 = "13033446617"
        self.phone5 = "13033446618"
        self.imgCode = "8888"
        self.pwd="1111aaaa"

    def tearDown(self):
        self.session.close()

    # @parameterized.expand(read_imgverify_data("imgverify.json"))
    @parameterized.expand(read_param_data("imgverify.json","test_get_img_verify_code","type,status_code"))
    def test01_get_img_code(self,type,status_code):
        #根据不同的type类型，准备不同的参数数据
        r=""
        if type=="float":
            r=str(random.random())
        elif type=="int":
            r=str(random.randint(10000000, 90000000))
        elif type=="char":
            r="".join(random.sample("kdkdkdweoodsoczodkr",5))
        # 调用接口类中的接口请求
        response=self.login_api.getImgCode(self.session,r)
        #接收接口的返回结果，进行断言
        self.assertEqual(200,response.status_code)

    # #参数为随机小数时获取图片验证码
    # def test01_get_img_code_random_float(self):
    #     #定义参数
    #     r=random.random()
    #     #调用接口类中的接口请求
    #     response=self.login_api.getImgCode(self.session,str(r))
    #     #接收接口的返回结果，进行断言
    #     self.assertEqual(200,response.status_code)
    #
    # #参数为随机整数时获取图片验证码成功
    # def test02_get_img_code_random_int(self):
    #     #定义参数
    #     r=random.randint(10000000,90000000)
    #     #调用接口类中的接口请求
    #     response=self.login_api.getImgCode(self.session,str(r))
    #     #接收接口的返回结果，进行断言
    #     self.assertEqual(200,response.status_code)
    #
    # #参数为空时获取图片验证码失败
    # def test03_get_img_code_param_is_null(self):
    #     # 定义参数
    #     r = ""
    #     # 调用接口类中的接口请求
    #     response=self.login_api.getImgCode(self.session,str(r))
    #     # 接收接口的返回结果，进行断言
    #     self.assertEqual(404,response.status_code)
    #
    # #参数为字母时获取图片验证码失败
    # def test04_get_img_code_param_is_char(self):
    #     # 定义参数
    #     r = "".join(random.sample("kdkdkdweoodsoczodkr",5))
    #     # 调用接口类中的接口请求
    #     response=self.login_api.getImgCode(self.session,str(r))
    #     # 接收接口的返回结果，进行断言
    #     self.assertEqual(400,response.status_code)

    #获取短信验证码成功-参数正确
    def test02_get_sms_code_success(self):
        #1、获取图片验证码
        # 定义参数
        r = random.randint(10000000, 90000000)
        # 调用接口类中的接口请求
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)
        #2、获取短信验证码
        # 定义参数
        # 调用接口类中的接口请求
        response=self.login_api.getSmsCode(self.phone1,self.imgCode,self.session)
        logging.info("--------------------------------get sms code response={}".format(response.json()))
        # 接收接口返回的结果，进行断言
        assert_utils(self,response,200,200,"短信发送成功")

    #获取短信验证码失败-图片验证码错误
    def test03_get_sms_code_wrong_img_code(self):
        # 1、获取图片验证码
        # 定义参数
        r = random.randint(10000000, 90000000)
        # 调用接口类中的接口请求
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)
        # 2、获取短信验证码
        # 定义参数
        # 调用接口类中的接口请求
        response = self.login_api.getSmsCode(self.phone1, "0000", self.session)
        logging.info("--------------------------------get sms code response={}".format(response.json()))
        # 接收接口返回的结果，进行断言
        assert_utils(self, response, 200, 100, "图片验证码错误")
    #获取短信验证码失败-图片验证码为空
    def test04_get_sms_code_img_code_is_null(self):
        # 1、获取图片验证码
        # 定义参数
        r = random.randint(10000000, 90000000)
        # 调用接口类中的接口请求
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)
        # 2、获取短信验证码
        # 定义参数
        # 调用接口类中的接口请求
        response = self.login_api.getSmsCode(self.phone1, "", self.session)
        logging.info("--------------------------------get sms code response={}".format(response.json()))
        # 接收接口返回的结果，进行断言
        assert_utils(self, response, 200, 100, "图片验证码错误")

    #获取短信验证码失败-手机号为空
    def test05_get_sms_code_phone_is_null(self):
        # 1、获取图片验证码
        # 定义参数
        r = random.randint(10000000, 90000000)
        # 调用接口类中的接口请求
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)
        # 2、获取短信验证码
        # 定义参数
        # 调用接口类中的接口请求
        response = self.login_api.getSmsCode("", self.imgCode, self.session)
        logging.info("--------------------------------get sms code response={}".format(response.json()))
        # 接收接口返回的结果，进行断言
        assert_utils(self, response, 200, 100, None)
    #获取短信验证码失败-未调用获取图片验证码接口
    def test06_get_sms_code_no_img_verify(self):
        # 获取短信验证码
        # 调用接口类中的接口请求
        response = self.login_api.getSmsCode(self.phone1, self.imgCode, self.session)
        logging.info("--------------------------------get sms code response={}".format(response.json()))
        # 接收接口返回的结果，进行断言
        assert_utils(self, response, 200, 100, "图片验证码错误")

    # @parameterized.expand(read_register_data("register.json"))
    @parameterized.expand(read_param_data("register.json","test_register","phone, password,invite_phone,verifycode,phone_code,dy_server,status_code,status,description"))
    def test07_register(self, phone, password,invite_phone,verifycode,phone_code,dy_server,status_code,status,description):
        #1、获取图片验证码
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
            response = self.login_api.getSmsCode(phone, verifycode, self.session)
            logging.info("--------------------------------get sms code response={}".format(response.json()))
            # 接收接口返回的结果，进行断言
            assert_utils(self, response, 200, 200, "短信发送成功")
            #3、注册成功
            # 定义参数
            # 调用接口类中的接口请求
            response = self.login_api.register(self.session,phone,password,invite_phone,verifycode,phone_code,dy_server)
            logging.info("--------------------------------get register response={}".format(response.json()))
            # 接收接口返回的结果，进行断言
            assert_utils(self, response, status_code, status, description)

    # # 输入必填项-注册成功
    # def test05_register_success_input_mandatory(self):
    #     # 1、获取图片验证码
    #     # 定义参数
    #     r = random.randint(10000000, 90000000)
    #     # 调用接口类中的接口请求
    #     response = self.login_api.getImgCode(self.session, str(r))
    #     print(response.status_code)
    #     # 接收接口的返回结果，进行断言
    #     self.assertEqual(200, response.status_code)
    #     # 2、获取短信验证码
    #     # 定义参数
    #     # 调用接口类中的接口请求
    #     response = self.login_api.getSmsCode(self.phone1, self.imgCode, self.session)
    #     logging.info("--------------------------------get sms code response={}".format(response.json()))
    #     # 接收接口返回的结果，进行断言
    #     assert_utils(self, response, 200, 200, "短信发送成功")
    #     #3、注册成功
    #     # 定义参数
    #     # 调用接口类中的接口请求
    #     response = self.login_api.register(self.session,self.phone1,self.pwd)
    #     logging.info("--------------------------------get register response={}".format(response.json()))
    #     # 接收接口返回的结果，进行断言
    #     assert_utils(self, response, 200, 200, "注册成功")
    #
    # # 输入全部参数-注册成功
    # def test06_register_success_input_all_params(self):
    #     # 1、获取图片验证码
    #     # 定义参数
    #     r = random.randint(10000000, 90000000)
    #     # 调用接口类中的接口请求
    #     response = self.login_api.getImgCode(self.session, str(r))
    #     # 接收接口的返回结果，进行断言
    #     self.assertEqual(200, response.status_code)
    #     # 2、获取短信验证码
    #     # 定义参数
    #     # 调用接口类中的接口请求
    #     response = self.login_api.getSmsCode(self.phone2, self.imgCode, self.session)
    #     logging.info("--------------------------------get sms code response={}".format(response.json()))
    #     # 接收接口返回的结果，进行断言
    #     assert_utils(self, response, 200, 200, "短信发送成功")
    #     #3、注册成功
    #     # 定义参数
    #     # 调用接口类中的接口请求
    #     response = self.login_api.register(self.session,self.phone2,self.pwd,invite_phone="15958585801")
    #     logging.info("--------------------------------get register response={}".format(response.json()))
    #     # 接收接口返回的结果，进行断言
    #     assert_utils(self, response, 200, 200, "注册成功")
    #
    # # 注册失败-手机号已存在
    # def test07_register_phone_is_exist(self):
    #     # 1、获取图片验证码
    #     # 定义参数
    #     r = random.randint(10000000, 90000000)
    #     # 调用接口类中的接口请求
    #     response = self.login_api.getImgCode(self.session, str(r))
    #     # 接收接口的返回结果，进行断言
    #     self.assertEqual(200, response.status_code)
    #     # 2、获取短信验证码
    #     # 定义参数
    #     # 调用接口类中的接口请求
    #     response = self.login_api.getSmsCode(self.phone2, self.imgCode, self.session)
    #     logging.info("--------------------------------get sms code response={}".format(response.json()))
    #     # 接收接口返回的结果，进行断言
    #     assert_utils(self, response, 200, 200, "短信发送成功")
    #     # 3、注册成功
    #     # 定义参数
    #     # 调用接口类中的接口请求
    #     response = self.login_api.register(self.session, self.phone2, self.pwd, invite_phone="15958585801")
    #     logging.info("--------------------------------get register response={}".format(response.json()))
    #     # 接收接口返回的结果，进行断言
    #     assert_utils(self, response, 200, 100, "手机已存在!")
    # # 注册失败-密码为空
    # def test08_register_password_is_null(self):
    #     # 1、获取图片验证码
    #     # 定义参数
    #     r = random.randint(10000000, 90000000)
    #     # 调用接口类中的接口请求
    #     response = self.login_api.getImgCode(self.session, str(r))
    #     # 接收接口的返回结果，进行断言
    #     self.assertEqual(200, response.status_code)
    #     # 2、获取短信验证码
    #     # 定义参数
    #     # 调用获取图片验证码接口
    #     # 调用接口类中的接口请求
    #     response = self.login_api.getSmsCode(self.phone3, self.imgCode, self.session)
    #     logging.info("--------------------------------get sms code response={}".format(response.json()))
    #     # 接收接口返回的结果，进行断言
    #     assert_utils(self, response, 200, 200, "短信发送成功")
    #     # 3、注册成功
    #     # 定义参数
    #     # 调用获取图片验证码接口
    #     # 调用接口类中的接口请求
    #     response = self.login_api.register(self.session, self.phone3, "", invite_phone="15958585801")
    #     logging.info("--------------------------------get register response={}".format(response.json()))
    #     # 接收接口返回的结果，进行断言
    #     assert_utils(self, response, 200, 100, "密码不能为空")
    #
    # # 注册失败-图片验证码错误
    # def test09_register_ImgCode_is_wrong(self):
    #     # 1、获取图片验证码
    #     # 定义参数
    #     r = random.randint(10000000, 90000000)
    #     # 调用接口类中的接口请求
    #     response = self.login_api.getImgCode(self.session, str(r))
    #     # 接收接口的返回结果，进行断言
    #     self.assertEqual(200, response.status_code)
    #     # 2、获取短信验证码
    #     # 定义参数
    #     # 调用获取图片验证码接口
    #     # 调用接口类中的接口请求
    #     response = self.login_api.getSmsCode(self.phone4, self.imgCode, self.session)
    #     logging.info("--------------------------------get sms code response={}".format(response.json()))
    #     # 接收接口返回的结果，进行断言
    #     assert_utils(self, response, 200, 200, "短信发送成功")
    #     # 3、注册成功
    #     # 定义参数
    #     # 调用获取图片验证码接口
    #     # 调用接口类中的接口请求
    #     response = self.login_api.register(self.session, self.phone4, self.pwd, invite_phone="15958585801",verifycode="8880")
    #     logging.info("--------------------------------get register response={}".format(response.json()))
    #     # 接收接口返回的结果，进行断言
    #     assert_utils(self, response, 200, 100, "验证码错误!")
    #
    #
    #
    # # 注册失败-短信验证码错误
    # def test10_register_SmsCode_is_wrong(self):
    #     # 1、获取图片验证码
    #     # 定义参数
    #     r = random.randint(10000000, 90000000)
    #     # 调用接口类中的接口请求
    #     response = self.login_api.getImgCode(self.session, str(r))
    #     # 接收接口的返回结果，进行断言
    #     self.assertEqual(200, response.status_code)
    #     # 2、获取短信验证码
    #     # 定义参数
    #     # 调用获取图片验证码接口
    #     # 调用接口类中的接口请求
    #     response = self.login_api.getSmsCode(self.phone4, self.imgCode, self.session)
    #     logging.info("--------------------------------get sms code response={}".format(response.json()))
    #     # 接收接口返回的结果，进行断言
    #     assert_utils(self, response, 200, 200, "短信发送成功")
    #     # 3、注册成功
    #     # 定义参数
    #     # 调用获取图片验证码接口
    #     # 调用接口类中的接口请求
    #     response = self.login_api.register(self.session, self.phone4, self.pwd, invite_phone="15958585801",phone_code="666660")
    #     logging.info("--------------------------------get register response={}".format(response.json()))
    #     # 接收接口返回的结果，进行断言
    #     assert_utils(self, response, 200, 100, "验证码错误")
    #
    # # 注册失败-不同意注册协议
    # def test11_register_noagree_protocol(self):
    #     # 1、获取图片验证码
    #     # 定义参数
    #     r = random.randint(10000000, 90000000)
    #     # 调用接口类中的接口请求
    #     response = self.login_api.getImgCode(self.session, str(r))
    #     # 接收接口的返回结果，进行断言
    #     self.assertEqual(200, response.status_code)
    #     # 2、获取短信验证码
    #     # 定义参数
    #     # 调用接口类中的接口请求
    #     response = self.login_api.getSmsCode(self.phone5, self.imgCode, self.session)
    #     logging.info("--------------------------------get sms code response={}".format(response.json()))
    #     # 接收接口返回的结果，进行断言
    #     assert_utils(self, response, 200, 200, "短信发送成功")
    #     # 3、注册成功
    #     # 定义参数
    #     # 调用获取图片验证码接口
    #     # 调用接口类中的接口请求
    #     response = self.login_api.register(self.session, self.phone2, self.pwd, invite_phone="15958585801",dy_server="off")
    #     logging.info("--------------------------------get register response={}".format(response.json()))
    #     # 接收接口返回的结果，进行断言
    #     assert_utils(self, response, 200, 100, "请同意我们的条款")

    #登录成功
    def test08_login_success(self):
        #定义参数
        #调用接口类中的接口
        response=self.login_api.login(self.session,keywords=self.phone2,password=self.pwd)
        logging.info("--------------------------------get login response={}".format(response.json()))
        #接收接口返回的结果，并进行断言
        assert_utils(self,response,200,200,"登录成功")

    #登录失败-用户不存在
    def test09_login_phone_not_exist(self):
        #定义参数
        wphone="17699991233"
        #调用接口类中的接口
        response=self.login_api.login(self.session,keywords=wphone,password=self.pwd)
        logging.info("--------------------------------get login response={}".format(response.json()))
        #接收接口返回的结果，并进行断言
        assert_utils(self,response,200,100,"用户不存在")

    #登录失败-密码为空
    def test10_login_password_is_null(self):
        #定义参数
        #调用接口类中的接口
        response=self.login_api.login(self.session,keywords=self.phone2,password="")
        logging.info("--------------------------------get login response={}".format(response.json()))
        #接收接口返回的结果，并进行断言
        assert_utils(self,response,200,100,"密码不能为空")

    #登录失败-密码错误
    def test11_login_password_is_wrong(self):
    #1、输入错误密码，提示错误1次
        #定义参数
        #调用接口类中的接口
        response=self.login_api.login(self.session,keywords=self.phone2,password="12121212")
        logging.info("--------------------------------get sms login response={}".format(response.json()))
        #接收接口返回的结果，并进行断言
        assert_utils(self,response,200,100,"密码错误1次,达到3次将锁定账户")
    #2、输入错误密码，提示错误2次
        #定义参数
        #调用接口类中的接口
        response=self.login_api.login(self.session,keywords=self.phone2,password="12121212")
        logging.info("--------------------------------get login response={}".format(response.json()))
        #接收接口返回的结果，并进行断言
        assert_utils(self,response,200,100,"密码错误2次,达到3次将锁定账户")
    #3、输入错误密码，提示被锁定
        #定义参数
        #调用接口类中的接口
        response=self.login_api.login(self.session,keywords=self.phone2,password="12121212")
        logging.info("--------------------------------get sms code response={}".format(response.json()))
        #接收接口返回的结果，并进行断言
        assert_utils(self,response,200,100,"由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")
    #4、输入正确密码，提示被锁定
        #定义参数
        #调用接口类中的接口
        response=self.login_api.login(self.session,keywords=self.phone2,password="1111aaaa")
        logging.info("--------------------------------get login response={}".format(response.json()))
        #接收接口返回的结果，并进行断言
        assert_utils(self,response,200,100,"由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")
    #5、等待60s，输入正确密码，提示登录成功
        #定义参数
        #调用接口类中的接口
        time.sleep(60)
        response=self.login_api.login(self.session,keywords=self.phone2,password="1111aaaa")
        logging.info("--------------------------------get login response={}".format(response.json()))
        #接收接口返回的结果，并进行断言
        assert_utils(self,response,200,200,"登录成功")









