# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwin.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(462, 268)
        mainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        mainWindow.setWindowOpacity(0.9)
        mainWindow.setAutoFillBackground(True)
        mainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 441, 211))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.horizontalLayoutWidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tableWidget_2 = QtWidgets.QTableWidget(self.horizontalLayoutWidget)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        self.verticalLayout_2.addWidget(self.tableWidget_2)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 462, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        self.menu_4 = QtWidgets.QMenu(self.menubar)
        self.menu_4.setObjectName("menu_4")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)
        self.action_2 = QtWidgets.QAction(mainWindow)
        self.action_2.setEnabled(True)
        self.action_2.setObjectName("action_2")
        self.action_4 = QtWidgets.QAction(mainWindow)
        self.action_4.setObjectName("action_4")
        self.action_6 = QtWidgets.QAction(mainWindow)
        self.action_6.setEnabled(False)
        self.action_6.setObjectName("action_6")
        self.action_7 = QtWidgets.QAction(mainWindow)
        self.action_7.setObjectName("action_7")
        self.action_8 = QtWidgets.QAction(mainWindow)
        self.action_8.setObjectName("action_8")
        self.action_9 = QtWidgets.QAction(mainWindow)
        self.action_9.setCheckable(True)
        self.action_9.setObjectName("action_9")
        self.action_10 = QtWidgets.QAction(mainWindow)
        self.action_10.setCheckable(True)
        self.action_10.setObjectName("action_10")
        self.action = QtWidgets.QAction(mainWindow)
        self.action.setObjectName("action")
        self.action_3 = QtWidgets.QAction(mainWindow)
        self.action_3.setObjectName("action_3")
        self.menu.addAction(self.action_2)
        self.menu.addSeparator()
        self.menu.addAction(self.action_4)
        self.menu.addAction(self.action)
        self.menu_2.addAction(self.action_7)
        self.menu_2.addAction(self.action_8)
        self.menu_4.addAction(self.action_3)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "绩效合约生成/汇总工具"))
        self.menu.setTitle(_translate("mainWindow", "模板"))
        self.menu_2.setTitle(_translate("mainWindow", "设置"))
        self.menu_3.setTitle(_translate("mainWindow", "导出"))
        self.menu_4.setTitle(_translate("mainWindow", "帮助"))
        self.action_2.setText(_translate("mainWindow", "绩效条目配置"))
        self.action_4.setText(_translate("mainWindow", "绩效汇总模板"))
        self.action_6.setText(_translate("mainWindow", "导出"))
        self.action_7.setText(_translate("mainWindow", "文件路径"))
        self.action_8.setText(_translate("mainWindow", "替换标签"))
        self.action_9.setText(_translate("mainWindow", "岗位绩效模板"))
        self.action_10.setText(_translate("mainWindow", "汇总模板"))
        self.action.setText(_translate("mainWindow", "岗位绩效模板"))
        self.action_3.setText(_translate("mainWindow", "关于"))
