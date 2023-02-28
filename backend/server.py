import logging
from logging.handlers import RotatingFileHandler

import waitress
import flask
import os

config = {'folder': 'files'}  # 定义文件存放的文件夹名称

app = flask.Flask(__name__)  # 创建flask应用对象并传入config字典
app.config.from_mapping(config)  # 从config字典中加载配置


@app.route('/upload', methods=['POST'])
def upload():
    # 文件上传接口
    file = flask.request.files.get('file')  # 获取文件对象
    if file:
        filename = file.filename  # 获取文件名
        folder = app.config.get('folder')  # 获取文件存放的文件夹名称
        filepath = os.path.join(os.getcwd(), folder, filename)  # 拼接相对路径
        file.save(filepath)  # 保存文件到指定目录下
        return f'File {filename} uploaded successfully.', 200  # 返回成功信息和状态码
    else:
        return 'No file found.', 400  # 返回错误信息和状态码


@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    # 文件下载接口
    directory = os.path.join(os.getcwd(), app.config.get('folder'))  # 拼接相对路径
    filepath = os.path.join(directory, filename)  # 拼接相对路径
    if os.path.exists(filepath):  # 判断文件是否存在
        return flask.send_from_directory(directory, filename)  # 发送指定目录下的指定文件
    else:
        return f'File {filename} not found.', 404  # 返回错误信息和状态码


@app.route('/delete/<filename>', methods=['DELETE'])
def delete(filename):
    # 文件删除接口
    filepath = os.path.join(os.getcwd(), app.config.get('folder'), filename)  # 拼接相对路径
    if os.path.exists(filepath):  # 判断文件是否存在
        os.remove(filepath)


if __name__ == '__main__':
    handler = RotatingFileHandler('flask.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

waitress.serve(app, host='0.0.0.0', port=5000, log_socket_errors=False)  # 启动服务
