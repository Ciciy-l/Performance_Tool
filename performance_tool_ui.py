# -*- coding: UTF-8 -*-
# by:Caiqiancheng
# Date:2023/2/7
import os
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

from com.common import read_config
from ui.mainwin import Ui_mainWindow as MainUi


# 主界面类
class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        # 初始化主界面
        self.main_ui = MainUi()
        self.main_ui.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        # 开始菜单项动作监听
        self.menu_action()

    def menu_action(self):
        """菜单栏动作监听"""
        # 绩效条目配置
        self.main_ui.action_2.triggered.connect(self.open_performance_item_config)
        # 汇总模板配置
        self.main_ui.action_4.triggered.connect(self.open_summary_template)
        # 岗位绩效模板


    def open_performance_item_config(self):
        """打开绩效条目配置表"""
        os.startfile(os.path.abspath(read_config("path").get("performance_item_table_path")))

    def open_summary_template(self):
        """打开汇总模板"""
        os.startfile(os.path.abspath(read_config("path").get("performance_summary_template_path")))

    def generate(self):
        pass

    def summary(self):
        pass


def show_gui():
    # 实例化一个应用对象
    app = QtWidgets.QApplication(sys.argv)
    # 实例化主界面类
    gui = MainWin()
    # 显示主界面窗口
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    # 启动GUI主线程
    show_gui()
