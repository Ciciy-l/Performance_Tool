# -*- coding: UTF-8 -*-

import configparser
import os


def read_config(section, filename="config.ini"):
    """
    读取配置文件
    """
    conf = configparser.RawConfigParser()
    with open(file="./com/{}".format(filename), mode="r", encoding="utf-8") as f:
        conf.read_file(f)
    return dict(conf.items(section))


def get_xlsx_filenames_list(directory_path):
    """
    获取指定目录下所有xlsx文件路径
    :param directory_path: 指定目录
    :return: xlsx文件名路径列表
    """
    filename_list = []
    filepath_list = []
    [filename_list.append(filename) for parent, dirname, filename in os.walk(directory_path, topdown=True)]
    [filepath_list.append(f"{directory_path}{filename}") for filename in filename_list[0]]
    return filepath_list
