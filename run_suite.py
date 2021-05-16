import unittest
import app
from lib.HTMLTestRunner_PY3 import HTMLTestRunner
from script.trust import Trust
from script.tender import Tender
# from script import Tr
from script.approve import Approve
from script.login_params import Login
import time
from app import BASE_DIR
from script.tender_process import test_tender_process

suite=unittest.TestSuite()
suite.addTest(unittest.makeSuite(Login))
suite.addTest(unittest.makeSuite(Approve))
suite.addTest(unittest.makeSuite(Trust))
suite.addTest(unittest.makeSuite(Tender))
suite.addTest(unittest.makeSuite(test_tender_process))


# report_file= BASE_DIR + "/report/report{}.html".format(time.strftime("%Y%m%D-%H%M%S"))
#report_file= BASE_DIR + "/report/report{}.html".format(time.strftime("%Y%m%d-%H%M%S")) 只在没用jenkins时才能这样写，用了jenkins的report名称就要固定，不能不断变化
report_file= BASE_DIR + "/report/report.html"
print(report_file)

with open(report_file,"wb") as f:
    runner=HTMLTestRunner(f,title="P2P金融项目测试报告",description="text")
    runner.run(suite)



