# -*- encoding=utf8 -*-
import unittest

from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco


x = '127.0.0.1:62001'

dev = connect_device(
    "Android:///%s?cap_method=CAP_METHOD.ADBCAP&&touch_method=TOUCH_METHOD.ADBTOUCH&&ime_method=IME_METHOD.ADBIME&&ori_method=ORI_METHOD.ADB" % x)


class TestMain(unittest.TestCase):

    def setUp(self):
        self.poco = AndroidUiautomationPoco(device=dev, use_airtest_input=True, screenshot_each_action=False)
        stop_app('com.yozo.office')
        start_app('com.yozo.office')

    def tearDown(self):
        stop_app('com.yozo.office')

    def test_01(self):
        self.poco("com.yozo.office:id/action_bar_root").wait_for_appearance(30)
        # self.poco()


if __name__ == '__main__':
    unittest.main()


