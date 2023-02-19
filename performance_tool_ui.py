# -*- coding: UTF-8 -*-
# by:Caiqiancheng
# Date:2023/2/7
import os
import shutil
import sys
import threading
from collections import Counter

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QMainWindow, QDialog, QMessageBox

from com.common import read_config
from performance_tool import generate_performance_table, summary_performance_table
from ui.mainwin import Ui_mainWindow as MainUi


class MainWin(QMainWindow):
    """主界面类"""

    def __init__(self):
        super().__init__()
        # 初始化主界面
        self.main_ui = MainUi()
        self.main_ui.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        # 初始化添加文件子窗口对象
        self.receive_interface = AddFile()
        # 初始化计时器
        self.timer = QTimer()
        # 开始菜单项动作监听线程
        threading.Thread(target=self.menu_action(), daemon=True).start()
        # 开始按钮点击监听线程
        threading.Thread(target=self.button_click(), daemon=True).start()
        # 开始listview显示监听线程
        threading.Thread(target=self.list_view(), daemon=True).start()

    def menu_action(self):
        """菜单栏动作监听"""
        # 绩效条目配置
        self.main_ui.action_2.triggered.connect(self.open_performance_item_config)
        # 汇总模板配置
        self.main_ui.action_4.triggered.connect(self.open_summary_template)
        # 岗位绩效模板
        self.main_ui.action.triggered.connect(self.open_performance_template)
        # 导出岗位绩效合约
        self.main_ui.action_5.triggered.connect(self.export_position_performance_contract)
        # 导出汇总绩效结果
        self.main_ui.action_11.triggered.connect(self.export_personnel_performance_summary)
        # 打开配置文件
        self.main_ui.action_12.triggered.connect(self.open_profile)
        # 关于
        self.main_ui.action_3.triggered.connect(self.about_information)

    def button_click(self):
        """按钮点击监听"""
        # 生成绩效合约
        self.main_ui.pushButton.clicked.connect(self.generate)
        # 汇总绩效结果
        self.main_ui.pushButton_2.clicked.connect(self.summary)
        # 添加文件
        self.main_ui.pushButton_3.clicked.connect(self.open_file_receiving_interface)


    def list_view(self):
        """listview显示监听"""
        # 计时器定时触发更新
        self.timer.start(1000)
        self.timer.timeout.connect(self.get_generated_performance_table)
        self.timer.timeout.connect(self.get_generating_performance_table)
        # 点击生成按钮时触发更新
        self.main_ui.pushButton.clicked.connect(self.get_generated_performance_table)
        self.main_ui.pushButton_2.clicked.connect(self.get_generating_performance_table)

    @staticmethod
    def open_performance_item_config():
        """打开绩效条目配置表"""
        os.startfile(os.path.abspath(read_config("path").get("performance_item_table_path")))

    @staticmethod
    def open_summary_template():
        """打开汇总模板"""
        os.startfile(os.path.abspath(read_config("path").get("performance_summary_template_path")))

    @staticmethod
    def open_performance_template():
        """打开岗位绩效表模板"""
        os.startfile(os.path.abspath(read_config("path").get("performance_template_path")))

    @staticmethod
    def open_profile():
        """打开配置文件"""
        os.startfile(os.path.abspath("./config.ini"))

    def generate(self):
        """调用生成功能"""
        generate_performance_table()
        QMessageBox.information(self, "OK!", "已成功生成绩效合约!\n可从菜单中导出!", QMessageBox.Yes)

    def summary(self):
        """调用汇总功能"""
        summary_performance_table()
        QMessageBox.information(self, "OK!", "已成功汇总绩效结果!\n可从菜单中导出!", QMessageBox.Yes)

    def open_file_receiving_interface(self):
        """打开接收文件汇总界面"""
        # 隐藏主界面显示
        self.hide()
        # 打开接收文件汇总窗口
        self.receive_interface.exec()
        # 恢复主界面显示
        self.show()

    def get_generated_performance_table(self):
        """读取已经生成绩效合约并显示"""
        # 读取已生成绩效合约文件列表
        file_list = os.listdir(os.path.abspath(read_config("path").get("performance_folder_path")))
        # 获取当前条目数
        item_count = self.main_ui.listWidget.count()
        # 获取条目列表
        item_list = [self.main_ui.listWidget.item(i).text() for i in range(item_count)]
        # 判断是否需要更新
        if not dict(Counter(file_list)) == dict(Counter(item_list)):
            self.main_ui.listWidget.clear()
            self.main_ui.listWidget.addItems(file_list)

    def get_generating_performance_table(self):
        """读取已存在的待汇总绩效表"""
        # 读取已生成绩效合约文件列表
        file_list = os.listdir(os.path.abspath(read_config("path").get("performance_summary_data_path")))
        # 获取当前条目数
        item_count = self.main_ui.listWidget_2.count()
        # 获取条目列表
        item_list = [self.main_ui.listWidget_2.item(i).text() for i in range(item_count)]
        # 判断是否需要更新
        if not dict(Counter(file_list)) == dict(Counter(item_list)):
            self.main_ui.listWidget_2.clear()
            self.main_ui.listWidget_2.addItems(file_list)

    def export_position_performance_contract(self):
        """导出岗位绩效合约"""
        # 获取岗位绩效合约文件路径
        otp_path = os.path.abspath(read_config("path").get("performance_folder_path"))
        if len(os.listdir(otp_path)) > 0:
            if self.save_file(otp_path, multi_file=True):
                QMessageBox.information(self, "导出", "已成功导出岗位绩效合约!", QMessageBox.Yes)
        else:
            QMessageBox.warning(self, "导出异常", "暂无可导出的绩效合约!\n请先尝试点击<生成绩效合约>按钮!",
                                QMessageBox.Yes)

    def export_personnel_performance_summary(self):
        """导出人员绩效汇总"""
        # 获取汇总结果文件路径
        otp_path = os.path.abspath(read_config("path").get("performance_summary_result_path"))
        # 汇总文件存在时执行导出功能,否则给出错误提示
        if os.path.isfile(otp_path):
            if self.save_file(otp_path):
                QMessageBox.information(self, "导出", "已成功导出人员绩效汇总!", QMessageBox.Yes)
        else:
            QMessageBox.warning(self, "导出异常", "暂无可导出的绩效汇总!\n请先尝试点击<汇总绩效结果>按钮!",
                                QMessageBox.Yes)

    def save_file(self, original_file_path, multi_file=False, opening=False):
        """保存文件/夹到指定路径"""
        # 获取目标文件夹路径
        opt_path = self.get_folder_path()
        if opt_path:
            if multi_file:
                # 读取文件列表
                file_list = os.listdir(original_file_path)
                for file in file_list:
                    shutil.copy(os.path.join(original_file_path, file), os.path.join(opt_path, file))
            else:
                shutil.copy(original_file_path, os.path.join(opt_path, os.path.basename(original_file_path)))
            if opening:
                os.startfile(opt_path)
            return True
        return False

    def about_information(self):
        """关于信息展示"""
        text = "软件名称:绩效生成汇总工具\n软件版本:V2.1(GUI)"
        QMessageBox.information(self, "关于", text, QMessageBox.Yes)

    def get_folder_path(self):
        # 弹出文件文件夹选择框,获取目标路径
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "选择导出文件夹", "./")
        return directory


class AddFile(QDialog):
    """拖入待汇总文件界面类"""

    def __init__(self, parent=None):
        super(AddFile, self).__init__(parent)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()
        self.setFixedSize(self.width(), self.height())

    def initUI(self):
        self.setAcceptDrops(True)
        self.setWindowTitle('请将需要汇总的文件或文件夹拖动到窗体内')
        self.resize(500, 310)
        self.setWindowOpacity(0.8)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_name = url.toLocalFile()
                target_path = os.path.abspath(read_config("path").get("performance_summary_data_path"))
                if os.path.isfile(file_name):
                    # 拷贝文件到指定目录
                    shutil.copy(file_name, target_path)
                elif os.path.isdir(file_name):
                    # 拷贝文件夹下的所有xlsx文件到指定目录
                    file_count = 0
                    for root, dirs, files in os.walk(file_name):
                        for file in files:
                            src_file = os.path.join(root, file)
                            # 仅拷贝xlsx文件
                            if src_file.endswith('.xlsx'):
                                shutil.copy(src_file, target_path)
                                file_count += 1
                            # print(src_file)
            self.close()


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
