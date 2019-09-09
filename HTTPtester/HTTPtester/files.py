# -*- coding: utf-8 -*-

from flask import render_template, request, make_response, jsonify
from flask_restful import reqparse
from . import app 
from data import datamanager
import tablib
import xlrd

ProjectNotExistErrMessage = {"ERRCOD": "ERRCOD", "ERRMSG": "项目不存在"} 
ALLOWED_EXTENSIONS = ['xlsx','xls']


@app.route('/testcases/upload', methods = ['GET','POST'])
def upload_file():
    '''读取用户上传的表格文档'''
    if request.method == 'POST':
        parser = reqparse.RequestParser()
        parser.add_argument('proj_id', type=str, required=True, location='form')
        parser.add_argument('file', type=str, required=True, location='files')
        args = parser.parse_args()
        file = request.files['file']

        if not datamanager.exist_proj_id(args.proj_id):
            return jsonify(ProjectNotExistErrMessage), 404

        if not file or not _allowed_file(file.filename):
            return jsonify({"ERRCOD": "ERR000",
                            "ERRMSG": "请上传excel文档"} ), 404
            
        cases = _read_upload(file)
        datamanager.add_testcases(args.proj_id, cases)
        return jsonify({"ERRCOD": "SUC000",
                        "ERRMSG": "请求成功"} )

    return render_template('upload.html')



@app.route('/testcases/download', methods = ['GET'])
def download_file():
    '''通过输入项目编号(proj_id)和测试案例编号(cid)提供用户导出测试案例信息的接口'''
    parser = reqparse.RequestParser()
    parser.add_argument('proj_id', type=str, required=True, location='args')
    parser.add_argument('cid', type=int, action='append', location='args')
    args = parser.parse_args()
    if not datamanager.exist_proj_id(args.proj_id):
        return jsonify(ProjectNotExistErrMessage), 404

    file = _download(args.proj_id,args.cid)
    if not file:
        return jsonify({"ERRCOD": "ERR000",
                            "ERRMSG": "文件读取失败"} )

    response = make_response(file)
    response.headers["Content-Disposition"] = f"attachment;filename={args.proj_id}.xlsx"
    response.headers['Content-Type'] = 'xlsx'
    return response
    



def _allowed_file(filename:str):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def _read_upload(file)->[list]:
    sheet = xlrd.open_workbook(file_contents=file.read()).sheets()[0]
    cases = []
    for i in range(1,sheet.nrows):
        if len(sheet.row_values(i)) == 8 and datamanager.is_valid_case(*sheet.row_values(i)):
            cases.append(sheet.row_values(i))
    return cases


def _download(proj_id: str, cids: [int]):
    data = []
    data.append(('name','method','url','request_header',
                'data','exp_status_code','assert_key','exp_value'))
    data += datamanager.get_testcases(proj_id, cids = cids, form = 'list')
    data = tablib.Dataset(*data)
    return data.xlsx



