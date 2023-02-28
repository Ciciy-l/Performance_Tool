from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QLineEdit, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
import requests


class FileApp(QWidget):

    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle('绩效合约管理')
        self.resize(400, 200)

        # 创建一个居中的label用来显示接口返回信息，默认为空白文本 
        self.label = QLabel('')
        self.label.setAlignment(Qt.AlignCenter)

        # 创建三个按钮并设置名称和功能 
        self.download_button = QPushButton('下载绩效合约')
        self.download_button.clicked.connect(self.show_download_line_edit)

        self.upload_button = QPushButton('上传绩效合约')
        self.upload_button.clicked.connect(self.upload_file)

        self.delete_button = QPushButton('删除绩效合约')
        self.delete_button.clicked.connect(self.show_delete_line_edit)

        # 创建一个水平布局并添加三个按钮 
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.download_button)
        self.button_layout.addWidget(self.upload_button)
        self.button_layout.addWidget(self.delete_button)

        # 创建两个文本框用来输入要下载或删除的文件名，默认隐藏
        # 给每个文本框添加回车键按下的事件处理函数
        self.download_line_edit = QLineEdit()
        self.download_line_edit.setPlaceholderText('请输入要下载的文件名')
        self.download_line_edit.hide()
        self.download_line_edit.returnPressed.connect(self.download_file)

        self.delete_line_edit = QLineEdit()
        self.delete_line_edit.setPlaceholderText('请输入要删除的文件名')
        self.delete_line_edit.hide()
        self.delete_line_edit.returnPressed.connect(self.delete_file)

        # 创建一个垂直布局并添加label、按钮布局和文本框
        # 注意这里只添加了一个占位符文本框，实际显示时会替换为对应的文本框
        # 这样做是为了保持布局的稳定性，避免切换文本框时窗口大小变化
        # 可以参考这个链接了解更多：https://stackoverflow.com/questions/4528347/prevent-window-resizing-with-pyqt
        self.placeholder_line_edit = QLineEdit()
        self.placeholder_line_edit.hide()

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.label)
        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addWidget(self.placeholder_line_edit)

        # 设置窗口的主布局为垂直布局
        self.setLayout(self.main_layout)

    def show_download_line_edit(self):
        # 显示下载文本框并隐藏删除文本框和占位符文本框
        # 清空label的内容
        self.download_line_edit.show()
        self.delete_line_edit.hide()
        self.placeholder_line_edit.hide()
        self.label.setText('')

    def show_delete_line_edit(self):
        # 显示删除文本框并隐藏下载文本框和占位符文本框
        # 清空label的内容
        self.delete_line_edit.show()
        self.download_line_edit.hide()
        self.placeholder_line_edit.hide()
        self.label.setText('')

    def download_file(self):
        # 调用下载文件的接口并在label显示响应信息
        # 获取下载文本框中输入的文件名
        filename = self.download_line_edit.text()

        if filename:
            url = f'http://localhost:5000/download/{filename}'
            response = requests.get(url)
            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    f.write(response.content)
                # 下载成功后清空下载文本框并隐藏它，显示占位符文本框
                # 在label显示成功信息
                self.download_line_edit.clear()
                self.download_line_edit.hide()
                self.placeholder_line_edit.show()
                self.label.setText(f'File {filename} downloaded successfully')
            else:
                # 下载失败时在label显示错误信息
                error_message = response.text
                self.label.setText(error_message)

    def upload_file(self):
        # 打开一个文件选择窗口，选好文件后调用文件上传接口
        # 清空label的内容
        self.label.setText('')
        # 获取要上传的文件路径和文件名
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select File')
        if file_path:
            # filename = os.path.basename(file_path)
            url = 'http://localhost:5000/upload'
            files = {'file': open(file_path, 'rb')}
            response = requests.post(url, files=files)
            # 上传成功或失败时在label显示响应信息
            message = response.text
            self.label.setText(message)

    def delete_file(self):
        # 调用删除文件的接口并在label显示响应信息
        # 获取删除文本框中输入的文件名
        filename = self.delete_line_edit.text()

        if filename:
            url = f'http://localhost:5000/delete/{filename}'
            response = requests.get(url)
            if response.status_code == 200:
                # 删除成功后清空删除文本框并隐藏它，显示占位符文本框
                # 在label显示成功信息
                self.delete_line_edit.clear()
                self.delete_line_edit.hide()
                self.placeholder_line_edit.show()
                self.label.setText(f'File {filename} deleted successfully')
            else:
                # 删除失败时在label显示错误信息
                error_message = response.text
                self.label.setText(error_message)


if __name__ == '__main__':
    app = QApplication([])
    window = FileApp()
    window.show()
    app.exec_()
