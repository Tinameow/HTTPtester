# -*- coding: utf-8 -*-

from flask import render_template, request, make_response, jsonify
from flask_restful import reqparse
from . import app 
from data import datamanager


ProjectNotExistErrMessage = {"ERRCOD": "ERRCOD", "ERRMSG": "项目不存在"} 


@app.route('/projects/',methods = ['GET'])
def list_projects():
    '''返回所有项目的名字(proj_name)、项目信息(proj_info)、和项目编号(proj_id)'''
    projects = datamanager.get_projects()
    return jsonify({"ERRCOD": "SUC000",
                    "ERRMSG": "请求成功",
                    "Projects": projects})



@app.route('/projects/add_proj', methods = ['GET','POST'])
def add_project():
    '''通过输入项目名称(proj_name)和项目描述(proj_info)添加项目，返回生成的项目编号(proj_id)'''
    if request.method == 'POST':
        parser = reqparse.RequestParser()
        parser.add_argument('proj_name', type=str, required=True, location=['form','json'])
        parser.add_argument('proj_info', type=str, location=['form','json'])
        args = parser.parse_args()

        if not _is_valid_proj_name(args.proj_name):
            return jsonify({"ERRCOD": "ERR000",
                            "ERRMSG": "项目名不合法"} )
            
        return jsonify({"ERRCOD": "SUC000",
                        "ERRMSG": "请求成功",
                        "proj_id": datamanager.add_proj(args.proj_name, args.proj_info)} )

    return render_template('add_proj.html')



@app.route('/projects/delete_proj', methods = ['GET'])
def delete_project():
    '''通过输入项目编号(proj_id)可以删除项目及项目相关的测试文档'''
    parser = reqparse.RequestParser()
    parser.add_argument('proj_id', type=str, required=True, location='args')
    args = parser.parse_args()

    if not datamanager.exist_proj_id(args.proj_id):
        return jsonify( ProjectNotExistErrMessage )

    datamanager.delete_proj(args.proj_id)
    return jsonify({"ERRCOD": "SUC000",
                    "ERRMSG": "请求成功"} )





def _is_valid_proj_name(proj_name:str) -> bool:
    return True


