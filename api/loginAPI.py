import app
import requests

class loginAPI():
    def __init__(self):
        self.getImgCode_url = app.BASE_URL + "/common/public/verifycode1/"
        self.getSmsCode_url=app.BASE_URL+"/member/public/sendSms"
        self.register_url=app.BASE_URL+"/member/public/reg"
        self.login_url=app.BASE_URL+"/member/public/login"

    def getImgCode(self,session,r):
        url=self.getImgCode_url + r
        return session.get(url)

    def getSmsCode(self,phone,imgVerifyCode,session):
        # 定义参数
        data={"phone":phone,
        "imgVerifyCode":imgVerifyCode,
        "type":"reg"}
        #发送请求并返回响应
        return session.post(self.getSmsCode_url,data=data)

    def register(self,session,phone,password,invite_phone="17091919002",verifycode="8888",phone_code="666666",dy_server="on"):
        #定义参数
        data={
                "phone": phone,
                "password": password,
                "verifycode": verifycode,
                "phone_code": phone_code,
                "dy_server": dy_server,
                "invite_phone": invite_phone,
        }
        #发送请求并返回响应
        return session.post(self.register_url,data=data)

    def login(self,session,keywords="13033446609",password='1111aaaa'):
        #定义参数
        data={
                "keywords": keywords,
                "password": password
        }
        #发送请求并返回响应
        return session.post(self.login_url,data=data)