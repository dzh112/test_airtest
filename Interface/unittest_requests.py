import time
import unittest
import requests
import paramunittest
import xlrd


# 封装一个读取Excel表格数据的函数
# 对Excel表格数据的读取需要用到一个库——xlrd库
def get_data(filename, sheetname):
    # 1. 打开Excel文件
    workbook = xlrd.open_workbook(filename)

    # 2. 打开Excel文件中的某张表
    sheet = workbook.sheet_by_name(sheetname)

    # 3. 读取表中的内容
    list = []
    for i in range(1, sheet.nrows):
        data = sheet.row_values(i)
        list.append(data)

    return list


list = get_data(r'D:\test_airtest\Interface\test.xls', '登录')
X = requests.post(url=list[1][1], data=list[1][4]).cookies['JSESSIONID']


# 2. 定义一个类，去继承unittest.TestCase
@paramunittest.parametrized(*list)  # 引用list中的所有数据
class FwLogin(unittest.TestCase):
    def setParameters(self, case_name, url, method, headers, params, assert_info):
        '''
        有多少条用例，这个函数就会执行多少次，每执行一条用例之前先会执行这个函数，把数据提取出来。
        :param case_name:
        :param url:
        :param method:
        :param headers:
        :param params:
        :param assert_info:
        :return:
        '''
        self.case_name = str(case_name)
        self.url = str(url)
        self.method = str(method)
        self.headers = str(headers)
        self.params = str(params)
        self.assert_info = str(assert_info)

    # 1. 实现一个用例方法
    def test_login_case(self):
        time.sleep(5)
        # 1. 组织参数
        self.headers = eval(self.headers)  # 将字符串转化为字典
        self.params = self.params
        self.headers[
            'Cookie'] = 'JSESSIONID=%s; access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiUk9MRV9Vc2VyIiwicGhvbmUiOiIxODAzNjg4ODUwMSIsInVzZXJfbmFtZSI6IiM5NjIwNSIsInNjb3BlIjpbIndlYi1hcHAiLCJ1c2VyaW5mbyJdLCJpZCI6Ijk2MjA1IiwiZXhwIjoxNTkwODMzMzU1LCJlbWFpbCI6ImR6aEB5b3pvc29mdC5jb20iLCJqdGkiOiI1ZjNkMTNhNS03NjQwLTQzYTAtYjQ5Ni01ZGM3OGRiMjNkZjciLCJjbGllbnRfaWQiOiJ3ZWItYXBwIn0.brO1U8pRXz98qO1fugSHzBKjkbFF_p2Z9sK3W_BBuRulV8u6qx2nXeI3N1baz0D6j_Nno4NnZ3etPoyfuJllmCaGtRcZFleW7-GYbtO2o3byDyNF3wUOs7qGvqpiZJ8cD2IkhW6_647qNoTBj2UbrN80tyNbShiz6fYUfQ6hkT8; refresh_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiUk9MRV9Vc2VyIiwicGhvbmUiOiIxODAzNjg4ODUwMSIsInVzZXJfbmFtZSI6IiM5NjIwNSIsInNjb3BlIjpbIndlYi1hcHAiLCJ1c2VyaW5mbyJdLCJhdGkiOiI1ZjNkMTNhNS03NjQwLTQzYTAtYjQ5Ni01ZGM3OGRiMjNkZjciLCJpZCI6Ijk2MjA1IiwiZXhwIjoxNTkxMzYyMTgxLCJlbWFpbCI6ImR6aEB5b3pvc29mdC5jb20iLCJqdGkiOiIxNGE2MTNmNy1hZjMwLTQzNTMtODUxYi0xNDQ3NDliZmY1YjQiLCJjbGllbnRfaWQiOiJ3ZWItYXBwIn0.VetM4N2oyT0_sjXxbHrRpN0zIN0-isaUHr-xxqj1fRzKhHrODOJVc9wQ9m7kLqlkAT1QnXuHQ1sX4Q_UKwOHDO2PklOFl7VyAqvKQj4LrxPVRUoOBjukbntRyMaHU2WoQVCOXS0Dnccm2HBJNYC3Zic2rOp60sQ3jNNusEHaKqI' % X
        # 2. 发请求
        if self.method == 'POST':
            # print(self.url, self.params, self.headers)
            response = requests.post(self.url, data=self.params.encode(), headers=self.headers)
        else:
            response = requests.get(self.url, params=self.params.encode(), headers=self.headers)

        # 3. 检查，断言
        # self.check_result(response)
        print(response.status_code)

    def check_result(self, response):
        '''
        断言  检查结果的
        :param response:
        :return:
        '''
        self.assert_info = eval(self.assert_info)  # 预期结果

        try:
            self.assertEqual(response.status_code, 200, '响应状态码错误')
            # self.assertEqual(response.reason, 'OK', '响应的响应码错误')
            self.assertEqual('操作成功' in response.json(), True, '响应的正文内容不一致！')
            print('%s测试用例通过！' % self.case_name)
        except AssertionError as e:
            print('%s测试用例不通过！%s' % (self.case_name, e))


if __name__ == '__main__':
    unittest.main()
