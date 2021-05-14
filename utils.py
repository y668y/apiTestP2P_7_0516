import json
import logging

import requests,pymysql
from bs4 import BeautifulSoup

import app


def assert_utils(self,response,status_code,status,description):
    self.assertEqual(status_code,response.status_code)
    print("status_code:",status_code, response.json().get("status_code"))
    # self.assertEqual(status_code, response.json().get("status_code"))
    print("status:",response.json().get("status"),"---",status)
    self.assertEqual(status,response.json().get("status"))
    print(response.json().get("description"))
    self.assertEqual(description, response.json().get("description"))

def third_request_api(form_data):
    # 解析form表单中的内容，并提取要用的参数
    soup = BeautifulSoup(form_data, "html.parser")
    third_url = soup.form["action"]
    logging.info("third request url={}".format(third_url))
    data = {}
    for input in soup.find_all("input"):
        data.setdefault(input["name"], input["value"])
    logging.info("third request data={}".format(data))
    # 发送第三方请求
    response = requests.post(third_url, data)
    return response

class DButils:
    @classmethod
    def get_conn(cls,db_name):
        conn=pymysql.connect(host=app.DB_URL,user=app.DB_USERNAME,password=app.DB_PASSWORD,db=db_name,autocommit=True)
        return conn

    @classmethod
    def close(cls,cursor=None,conn=None):
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    @classmethod
    def delete(cls,db_name,sql):
        try:
            conn=cls.get_conn(db_name)
            cursor=conn.cursor()
            cursor.execute(sql)
        except Exception as e:
            conn.rollback()
        finally:
            cls.close(cursor,conn)


def read_imgverify_data(file_name):
    file=app.BASE_DIR+"/data/"+file_name
    test_case_data=[]
    with open(file,encoding="utf-8") as f:
        verify_data=json.load(f) #将json格式文件转换为字典格式
        test_data_list=verify_data.get("test_get_img_verify_code")
        for test_data in test_data_list:
            test_case_data.append((test_data.get("type"),test_data.get("status_code")))
        print("json.data={}".format(test_case_data))
    return test_case_data

def read_register_data(file_name):
    file=app.BASE_DIR+"/data/"+file_name
    test_case_data=[]
    with open(file,encoding="utf-8") as f:
        verify_data=json.load(f) #将json格式文件转换为字典格式
        test_data_list=verify_data.get("test_register")
        for test_data in test_data_list:
            test_case_data.append((test_data.get("phone"),test_data.get("password"),test_data.get("invite_phone"),test_data.get("verifycode"),test_data.get("phone_code"),test_data.get("dy_server"),test_data.get("status_code"),test_data.get("status"),test_data.get("description")))
        print("json.data={}".format(test_case_data))
    return test_case_data

#定义统一读取参数文件的方法
def read_param_data(file_name,method_name,param_names):
    """

    :param file_name: 参数文件名字
    :param method_name: 参数里每组数据的解释名称
    :param param_names: 每组参数数据组成的字符串，如""type,status_code
    :return:
    """
    file=app.BASE_DIR+"/data/"+file_name
    test_case_data=[]
    with open(file,encoding="utf-8") as f:
        file_data=json.load(f) #将json格式文件转换为字典格式
        test_data_list=file_data.get(method_name)
        for test_data in test_data_list:
            test_params=[]
            for param in param_names.split(","):
                test_params.append(test_data.get(param))
            test_case_data.append(test_params)
        print("json.data={}".format(test_case_data))
    return test_case_data









