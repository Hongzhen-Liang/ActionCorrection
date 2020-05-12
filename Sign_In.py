# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Sign_In.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(396, 199)
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(73, 52, 261, 103))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setMinimumSize(QtCore.QSize(0, 30))
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setMinimumSize(QtCore.QSize(0, 30))
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.login_username = QtWidgets.QLineEdit(self.layoutWidget)
        self.login_username.setObjectName("login_username")
        self.gridLayout.addWidget(self.login_username, 0, 1, 1, 2)
        self.login_psw = QtWidgets.QLineEdit(self.layoutWidget)
        self.login_psw.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login_psw.setObjectName("login_psw")
        self.gridLayout.addWidget(self.login_psw, 1, 1, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(90, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_login = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_login.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btn_login.setObjectName("btn_login")
        self.horizontalLayout.addWidget(self.btn_login)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btn_register = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_register.setMinimumSize(QtCore.QSize(40, 0))
        self.btn_register.setMaximumSize(QtCore.QSize(60, 16777215))
        self.btn_register.setIconSize(QtCore.QSize(5, 5))
        self.btn_register.setObjectName("btn_register")
        self.horizontalLayout.addWidget(self.btn_register)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        self.btn_login.clicked.connect(Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_2.setText(_translate("Dialog", "密码："))
        self.label.setText(_translate("Dialog", "用户名："))
        self.btn_login.setText(_translate("Dialog", "登录"))
        self.btn_register.setText(_translate("Dialog", "注册"))
