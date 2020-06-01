import time
import unittest
import requests
import paramunittest
import xlrd


# ��װһ����ȡExcel������ݵĺ���
# ��Excel������ݵĶ�ȡ��Ҫ�õ�һ���⡪��xlrd��
def get_data(filename, sheetname):
    # 1. ��Excel�ļ�
    workbook = xlrd.open_workbook(filename)

    # 2. ��Excel�ļ��е�ĳ�ű�
    sheet = workbook.sheet_by_name(sheetname)

    # 3. ��ȡ���е�����
    list = []
    for i in range(1, sheet.nrows):
        data = sheet.row_values(i)
        list.append(data)

    return list


list = get_data(r'D:\test_airtest\Interface\test.xls', '��¼')
X = requests.post(url=list[1][1], data=list[1][4]).cookies['JSESSIONID']


# 2. ����һ���࣬ȥ�̳�unittest.TestCase
@paramunittest.parametrized(*list)  # ����list�е���������
class FwLogin(unittest.TestCase):
    def setParameters(self, case_name, url, method, headers, params, assert_info):
        '''
        �ж�������������������ͻ�ִ�ж��ٴΣ�ÿִ��һ������֮ǰ�Ȼ�ִ�������������������ȡ������
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

    # 1. ʵ��һ����������
    def test_login_case(self):
        time.sleep(5)
        # 1. ��֯����
        self.headers = eval(self.headers)  # ���ַ���ת��Ϊ�ֵ�
        self.params = self.params
        self.headers[
            'Cookie'] = 'JSESSIONID=%s; access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiUk9MRV9Vc2VyIiwicGhvbmUiOiIxODAzNjg4ODUwMSIsInVzZXJfbmFtZSI6IiM5NjIwNSIsInNjb3BlIjpbIndlYi1hcHAiLCJ1c2VyaW5mbyJdLCJpZCI6Ijk2MjA1IiwiZXhwIjoxNTkwODMzMzU1LCJlbWFpbCI6ImR6aEB5b3pvc29mdC5jb20iLCJqdGkiOiI1ZjNkMTNhNS03NjQwLTQzYTAtYjQ5Ni01ZGM3OGRiMjNkZjciLCJjbGllbnRfaWQiOiJ3ZWItYXBwIn0.brO1U8pRXz98qO1fugSHzBKjkbFF_p2Z9sK3W_BBuRulV8u6qx2nXeI3N1baz0D6j_Nno4NnZ3etPoyfuJllmCaGtRcZFleW7-GYbtO2o3byDyNF3wUOs7qGvqpiZJ8cD2IkhW6_647qNoTBj2UbrN80tyNbShiz6fYUfQ6hkT8; refresh_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiUk9MRV9Vc2VyIiwicGhvbmUiOiIxODAzNjg4ODUwMSIsInVzZXJfbmFtZSI6IiM5NjIwNSIsInNjb3BlIjpbIndlYi1hcHAiLCJ1c2VyaW5mbyJdLCJhdGkiOiI1ZjNkMTNhNS03NjQwLTQzYTAtYjQ5Ni01ZGM3OGRiMjNkZjciLCJpZCI6Ijk2MjA1IiwiZXhwIjoxNTkxMzYyMTgxLCJlbWFpbCI6ImR6aEB5b3pvc29mdC5jb20iLCJqdGkiOiIxNGE2MTNmNy1hZjMwLTQzNTMtODUxYi0xNDQ3NDliZmY1YjQiLCJjbGllbnRfaWQiOiJ3ZWItYXBwIn0.VetM4N2oyT0_sjXxbHrRpN0zIN0-isaUHr-xxqj1fRzKhHrODOJVc9wQ9m7kLqlkAT1QnXuHQ1sX4Q_UKwOHDO2PklOFl7VyAqvKQj4LrxPVRUoOBjukbntRyMaHU2WoQVCOXS0Dnccm2HBJNYC3Zic2rOp60sQ3jNNusEHaKqI' % X
        # 2. ������
        if self.method == 'POST':
            # print(self.url, self.params, self.headers)
            response = requests.post(self.url, data=self.params.encode(), headers=self.headers)
        else:
            response = requests.get(self.url, params=self.params.encode(), headers=self.headers)

        # 3. ��飬����
        # self.check_result(response)
        print(response.status_code)

    def check_result(self, response):
        '''
        ����  �������
        :param response:
        :return:
        '''
        self.assert_info = eval(self.assert_info)  # Ԥ�ڽ��

        try:
            self.assertEqual(response.status_code, 200, '��Ӧ״̬�����')
            # self.assertEqual(response.reason, 'OK', '��Ӧ����Ӧ�����')
            self.assertEqual('�����ɹ�' in response.json(), True, '��Ӧ���������ݲ�һ�£�')
            print('%s��������ͨ����' % self.case_name)
        except AssertionError as e:
            print('%s����������ͨ����%s' % (self.case_name, e))


if __name__ == '__main__':
    unittest.main()
