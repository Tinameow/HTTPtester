# -*- coding: utf-8 -*-

from data import datamanager
import requests 
import json
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed


loggerfile = 'errorcases.log'



def run(tid):
    '''run the test by testing the case one by one'''
    #testcases = datamanager.get_testcases(tid, form = 'list')
    #for i , case in enumerate(testcases,1):
    #    datamanager.update_test_result(tid, i, test(*case[1:8]))

    testcases = datamanager.get_testcases(tid, form = 'list')
    with ProcessPoolExecutor(max_workers = 10) as executor:
        try:
            future_to_num = {executor.submit(test,*case[1:8]):num for num, case in enumerate(testcases, 1)}
            for future in as_completed(future_to_num):
                num = future_to_num[future]
                datamanager.update_test_result(tid, num, future.result())
        except Exception as e:
            f = open(loggerfile, 'a')
            f.write(f"====={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}=====\n")
            f.write(f'{str(e)}>>>({tid}){case}\n')
            f.close()       


def test(method, url, req_header, data, exp_status_code, assert_key, exp_value)->tuple:
    '''send the request, get the response, and return the test result'''
    try:
        # 去掉url的空格，为不以http开头的url添加http
        url = _get_legal_url(url)
        # 判断data和req_header是否为json格式
        if (data and method == "POST" and not _is_json(data)) or (req_header and not _is_json(req_header)):
            return ('','','Data or headers should be in json format','SKIPPED')

        # 将data和req_header转换为字典
        data = eval(data) if data else {}
        req_header = eval(req_header) if req_header else {}

        # 根据方法发送请求
        if method == "POST":
            response = requests.post(url,data = data, headers = req_header, timeout = 10) 
        elif method == "GET":
            response = requests.get(url,headers = req_header, timeout = 10)
        else:
            response = requests.request(method, url, headers = req_header, data = data, timeout = 10)


        # 进行状态码测试和断言项测试
        status_test = (not exp_status_code and  response.status_code == 200 ) \
                        or (exp_status_code == str(response.status_code))
        key_value_test = not assert_key or (exp_value in _get_value(assert_key, response.json()))

        # 返回结果
        return (response.status_code, response.json()[assert_key] if assert_key else '', 
                response.text[:1024], 'PASS' if (status_test and key_value_test) else 'FAIL')

    # 请求报错则返回错误原因
    except requests.exceptions.RequestException as e:
        return ('','',str(e),'ERROR')
    
    # 响应的text不是json格式的，则根据状态码的测试返回判断
    except json.decoder.JSONDecodeError:
        return (response.status_code,'',response.text[:1024],'PASS' if status_test else 'FAIL')
    
    # 如果有其他错误则写入log文档
    except Exception as e:
        f = open(loggerfile, 'a')
        f.write(f"====={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}=====\n")
        f.write(f'{str(e)}>>>{method}, {url}, {req_header}, {data}, {exp_status_code}, {assert_key}, {exp_value}\n')
        f.close()
        return ('','','','SKIPPED')




def _get_legal_url(url):
    '''return a legal url'''
    url = url.strip()
    if not url.startswith('http'):
        url = 'http://' + url
    return url



def _is_json(data) -> bool:
    '''if the data is in json format, return true; else return false'''
    try:
        s = json.loads(data)
    except json.decoder.JSONDecodeError:
        return False
    else:
        return True
   

def _get_values(key:str, d:dict) ->[]:
    '''search the key in a dictionary, return the corresponding value(s)'''
    result=[]
    if key in d:
        result.append( d[key])
    for sub in d.values():
        if type(sub) is list:
            for sub_d in sub:
                if type(sub_d) is dict:
                    result+=_get_values(key, sub_d)
        elif type(sub) is dict:
                result+=_get_values(key, sub)
    return result
