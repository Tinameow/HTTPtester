# -*- coding: utf-8 -*-

from data import datamanager
import requests 
import json
import time


def run(tid):
    testcases = datamanager.get_testcases(tid, form = 'list')
    for i, case in enumerate(testcases,1):
        time.sleep(10)
        datamanager.update_test_result(tid, i, test(*case[1:8]))
        
    print('done')


def test(method, url, req_header, data, exp_status_code, assert_key, exp_value):
    try:
        if method == "POST":
                response = requests.post(url,data = data,headers = req_header, timeout = 10)
        elif method == "GET":
            response = requests.get(url,headers = req_header, timeout = 10)

        status_test = not exp_status_code or (exp_status_code == response.status_code)
        key_value_test = not assert_key or (exp_value == response.json()[assert_key])

        return (response.status_code, response.json()[assert_key], 
                response.text, 'PASS' if (status_test and key_value_test) else 'FAIL')
    except requests.exceptions.RequestException and requests.exceptions.MissingSchema as e:
        return ('','',str(e),'ERROR')
    except json.decoder.JSONDecodeError:
        return (response.status_code,'',response.text,'PASS' if status_test else 'FAIL')
    except:
        return ('','','','ERROR')

