# -*- coding: utf-8 -*-

import unittest
import xlrd, openpyxl
import os
import json
from HTTPtester import app 

WORKBOOK = 'data/projectmanager.xlsx'
DATADIR = 'data'
URL = 'http://127.0.0.1:5000/'

class TestAPI(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_get_projects(self):
        url = URL + 'projects'
        exp_response = '{"ERRCOD": "SUC000", "ERRMSG": "请求成功", "Projects": []}'
        response = self.client().get(url).text
        self.assertEqual(response, exp_response)
        

    def tearDown(self):
        for filename in os.listdir(DATADIR):
            if '.xlsx' in filename:
                os.remove(os.path.join(DATADIR,filename))
        workbook = openpyxl.Workbook()
        workbook['Sheet'].append(["proj_id","proj_name","proj_info"])
        workbook.save(WORKBOOK)

if __name__ == '__main__':
    unittest.main()
