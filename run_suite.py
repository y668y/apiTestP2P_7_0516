import unittest
import app
from lib.HTMLTestRunner_PY3 import HTMLTestRunner
from script import trust, tender
from script.approve import Approve
from script.login_params import Login
import time
from app import BASE_DIR
from script.tender_process import test_tender_process

suite=unittest.TestSuite()
suite.addTest(unittest.makeSuite(Login))
suite.addTest(unittest.makeSuite(Approve))
suite.addTest(unittest.makeSuite(trust))
suite.addTest(unittest.makeSuite(tender))
suite.addTest(unittest.makeSuite(test_tender_process))


# report_file= BASE_DIR + "/report/report{}.html".format(time.strftime("%Y%m%D-%H%M%S"))
report_file= BASE_DIR + "/report/report{}.html".format(time.strftime("%Y%m%d-%H%M%S"))
print(report_file)

with open(report_file,"wb") as f:
    runner=HTMLTestRunner(f,title="P2P金融项目测试报告",description="text")
    runner.run(suite)



