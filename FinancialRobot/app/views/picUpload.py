# encoding:utf-8
# !/usr/bin/env python
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, make_response, send_from_directory, abort
import os
import json
from app.utils.pic_str import *
from app.utils.res_json import *

up = Blueprint("up", __name__)
UPLOAD_FOLDER = '../upload'
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = {'png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF'}
MAX_CONTENT_LENGTH = 1 * 1024 * 1024  # 1MB


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@up.route('/')
def upload_test():
    return render_template('up.html')


# 上传文件
@up.route('/upload', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, UPLOAD_FOLDER)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['photo']
    size = len(f.read())
    print(size)
    f.seek(0)
    if f and allowed_file(f.filename):
        if size <= MAX_CONTENT_LENGTH:
            fname = secure_filename(f.filename)
            print(fname)
            ext = fname.rsplit('.', 1)[1]
            new_filename = Pic_str().create_uuid() + '.' + ext
            f.save(os.path.join(file_dir, new_filename))
            f.close()
            return json.dumps(return_success({"new_filename": new_filename}), ensure_ascii=False)
        else:
            return json.dumps(return_unsuccess("文件大小超出1MB"),ensure_ascii=False)
    else:
        return json.dumps(return_unsuccess("文件格式不正确"), ensure_ascii=False)


@up.route('/download/<string:filename>', methods=['GET'])
def download(filename):
    if request.method == "GET":
        file_dir = os.path.join(basedir, UPLOAD_FOLDER)
        print(file_dir)
        if os.path.isfile(os.path.join(file_dir, filename)):
            return send_from_directory(file_dir, filename, as_attachment=True)
        pass


# show photo
@up.route('/show/<string:filename>', methods=['GET'])
def show_photo(filename):
    file_dir = os.path.join(basedir, UPLOAD_FOLDER)
    if request.method == 'GET':
        if filename is None:
            pass
        else:
            image_data = open(os.path.join(file_dir, '%s' % filename), "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response
    else:
        pass
