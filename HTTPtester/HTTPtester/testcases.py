# -*- coding: utf-8 -*-


from flask import render_template, request, make_response, jsonify
from flask_restful import reqparse
from . import app 
from data import datamanager
import tablib
import xlrd


ProjectNotExistErrMessage = {"ERRCOD": "ERRCOD", "ERRMSG": "项目不存在"} 


@app.route('/testcases', methods = ['GET'])
def search_testcases():
    '''
    通过输入项目编号(proj_id)和关键词(search_key)筛选并返回测试案例的信息;
    如果关键词为空，则返回全部案例信息。
    '''
    parser = reqparse.RequestParser()
    parser.add_argument('proj_id', type=str, required=True, location='args')
    parser.add_argument('search_key', type=str, location=['args','form'])
    args = parser.parse_args()

    if not datamanager.exist_proj_id(args.proj_id):
        return jsonify(ProjectNotExistErrMessage), 404

    data = datamanager.get_testcases(args.proj_id, args.search_key)
    return jsonify({"ERRCOD": "SUC000",
                    "ERRMSG": "请求成功",
                    "Testcases": data} )
    


@app.route('/testcases/addcase', methods = ['GET','POST'])
def add_case():
    '''
    添加案例
    '''
    if request.method == 'POST':
        parser = reqparse.RequestParser()
        parser.add_argument('proj_id', type=str, required=True, location='form')
        parser.add_argument('name', type=str, required=True, location='form')
        parser.add_argument('method', type=str, required=True, location='form')
        parser.add_argument('url', type=str, required=True, location='form')
        parser.add_argument('req_header', type=str, location='form')
        parser.add_argument('data', type=str, location='form')
        parser.add_argument('exp_status_code', type=str, location='form')
        parser.add_argument('assert_key', type=str, location='form')
        parser.add_argument('exp_value', type=str, location='form')
        args = parser.parse_args()
        

        if not datamanager.exist_proj_id(args.proj_id):
            return jsonify(ProjectNotExistErrMessage), 404

        if not datamanager.is_valid_case(args.name, args.method, args.url, 
                                          args.req_header, args.data, args.exp_status_code,
                                          args.assert_key, args.exp_value):
            return jsonify({"ERRCOD": "ERR000",
                       "ERRMSG": "参数不合法"} ), 404

        datamanager.add_testcases(args.proj_id, [[args.name, args.method, args.url, 
                                              args.req_header, args.data, args.exp_status_code,
                                              args.assert_key, args.exp_value]])
        return jsonify({"ERRCOD": "SUC000",
                        "ERRMSG": "请求成功"} )

    return render_template('add_case.html')





@app.route('/testcases/delete',methods = ['GET'])
def delete_cases():
    '''通过输入项目编号proj_id和测试案例编号cid，删除案例信息'''
    parser = reqparse.RequestParser()
    parser.add_argument('proj_id', type=str, required=True, location='args')
    parser.add_argument('cid', type=int, required=True, action='append', location='args')
    args = parser.parse_args()

    if not datamanager.exist_proj_id(args.proj_id):
        return jsonify(ProjectNotExistErrMessage), 404

    datamanager.delete_cases(args.proj_id,args.cid)

    return jsonify({"ERRCOD": "SUC000",
                    "ERRMSG": "请求成功"} )

    






