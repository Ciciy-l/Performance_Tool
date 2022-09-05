# -*- coding: UTF-8 -*-

import configparser


def read_config(section, filename="config.ini"):
    """
    读取配置文件
    """
    conf = configparser.ConfigParser()
    with open(file="./com/{}".format(filename), mode="r", encoding="utf-8") as f:
        conf.read_file(f)
    return dict(conf.items(section))
