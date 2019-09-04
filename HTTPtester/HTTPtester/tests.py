# -*- coding: utf-8 -*-

from flask import render_template, request, make_response, jsonify
from flask_restful import reqparse
from . import app, runtests
from data import datamanager
from concurrent.futures import ThreadPoolExecutor
from collections import OrderedDict


ProjectNotExistErrMessage = OrderedDict({"ERRCOD": "ERRCOD", "ERRMSG": "项目不存在"})

executor = ThreadPoolExecutor(1)


@app.route('/testcases/test',methods=['GET'])
def test_cases():
    '''通过输入项目编号proj_id和测试案例编号cid开始测试'''
    parser = reqparse.RequestParser()
    parser.add_argument('proj_id', type=str, required=True, location='args')
    parser.add_argument('cid', type=int, action='append', location='args')
    args = parser.parse_args()

    if not datamanager.exist_proj_id(args.proj_id):
        return jsonify(ProjectNotExistErrMessage), 404

    tid = datamanager.create_test(args.proj_id,args.cid)
    executor.submit(runtests.run,tid)
    return jsonify({"ERRCOD": "SUC000",
                        "ERRMSG": "请求成功",
                        "tid": tid} )



@app.route('/tests',methods = ['GET'])
def list_tests():
    '''返回所有测试的信息'''
    parser = reqparse.RequestParser()
    parser.add_argument('proj_id', type=str, required=True, location='args')
    args = parser.parse_args()

    if not datamanager.exist_proj_id(args.proj_id):
        return jsonify(ProjectNotExistErrMessage),404
        
    return jsonify({"ERRCOD": "SUC000",
                    "ERRMSG": "请求成功",
                    "Projects": datamanager.get_tests(args.proj_id)})




@app.route('/testresult', methods = ['GET'])
def get_test():
    '''返回单个测试的信息'''
    parser = reqparse.RequestParser()
    parser.add_argument('tid', type=str, required=True, location='args')
    args = parser.parse_args()
    tid = args.tid

    if not datamanager.exist_tid(tid):
        return jsonify(ProjectNotExistErrMessage),404

    info = datamanager.get_test(tid)
    if info['status'] != 'Done':
        return jsonify(info)

    return jsonify({"ERRCOD": "SUC000",
                    "ERRMSG": "请求成功",
                    "Projects": datamanager.get_testcases(tid)})



    



