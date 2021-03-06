# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chapterList.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_widget_chapterList(object):
    def setupUi(self, widget_chapterList):
        widget_chapterList.setObjectName("widget_chapterList")
        widget_chapterList.resize(372, 548)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        widget_chapterList.setFont(font)
        widget_chapterList.setStyleSheet("QPushButton#btn_ok,\n"
"QPushButton#btn_cancle\n"
"{\n"
"      /* 文字颜色 */\n"
"        color: #0099CC; \n"
"      /* 清除背景色 */\n"
"        background: transparent; \n"
"      /* 边框样式、颜色、宽度 */\n"
"        border: 2px solid #0099CC;\n"
"      /* 给边框添加圆角 */\n"
"        border-radius: 6px; \n"
"      /* 字母转大写 */\n"
"        border: none;\n"
"        color: white;\n"
"        padding: 6px 12px;\n"
"        text-align: center;\n"
"        display: inline-block;\n"
"        font-size: 15px;\n"
"        margin: 4px 2px;\n"
"        -webkit-transition-duration: 0.4s; /* Safari */\n"
"        transition-duration: 0.4s;\n"
"        cursor: pointer;\n"
"        text-decoration: none;\n"
"        text-transform: uppercase;\n"
"\n"
"        background-color: white; \n"
"        color: black; \n"
"        border: 2px solid #008CBA;\n"
"}\n"
"\n"
"/* 悬停样式 */\n"
"QPushButton#btn_ok:hover,\n"
"QPushButton#btn_cancle:hover\n"
"{\n"
"        background-color: #008CBA;\n"
"        color: white;\n"
"}\n"
"/*按下样式*/\n"
"QPushButton#btn_ok:pressed,\n"
"QPushButton#btn_cancle:pressed\n"
"{\n"
"        padding-left:16px;\n"
"        padding-top:9px;\n"
"}\n"
"QWidget#widget_chapterList{\n"
"    background-color:white;\n"
"}\n"
"QListWidget#listWidget{\n"
"border:0px solid #000000;\n"
"background-color: rgba(255, 255, 224, 10%);\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(widget_chapterList)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(widget_chapterList)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.hlay_main = QtWidgets.QHBoxLayout(self.frame)
        self.hlay_main.setContentsMargins(11, 0, 11, 0)
        self.hlay_main.setSpacing(0)
        self.hlay_main.setObjectName("hlay_main")
        self.listWidget = QtWidgets.QListWidget(self.frame)
        self.listWidget.setStyleSheet("")
        self.listWidget.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listWidget.setObjectName("listWidget")
        self.hlay_main.addWidget(self.listWidget)
        self.verticalLayout.addWidget(self.frame)
        self.frame_checkbox = QtWidgets.QFrame(widget_chapterList)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        self.frame_checkbox.setFont(font)
        self.frame_checkbox.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_checkbox.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_checkbox.setObjectName("frame_checkbox")
        self.hlay_checkbox = QtWidgets.QHBoxLayout(self.frame_checkbox)
        self.hlay_checkbox.setContentsMargins(12, 0, 11, 0)
        self.hlay_checkbox.setObjectName("hlay_checkbox")
        self.checkBox_all_check = QtWidgets.QCheckBox(self.frame_checkbox)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        self.checkBox_all_check.setFont(font)
        self.checkBox_all_check.setObjectName("checkBox_all_check")
        self.hlay_checkbox.addWidget(self.checkBox_all_check)
        self.verticalLayout.addWidget(self.frame_checkbox)
        self.frame_checkbox_auto = QtWidgets.QFrame(widget_chapterList)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        self.frame_checkbox_auto.setFont(font)
        self.frame_checkbox_auto.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_checkbox_auto.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_checkbox_auto.setObjectName("frame_checkbox_auto")
        self.hlay_auto = QtWidgets.QHBoxLayout(self.frame_checkbox_auto)
        self.hlay_auto.setContentsMargins(12, 0, 11, 0)
        self.hlay_auto.setObjectName("hlay_auto")
        self.checkBox_check_auto = QtWidgets.QCheckBox(self.frame_checkbox_auto)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        self.checkBox_check_auto.setFont(font)
        self.checkBox_check_auto.setObjectName("checkBox_check_auto")
        self.hlay_auto.addWidget(self.checkBox_check_auto)
        self.verticalLayout.addWidget(self.frame_checkbox_auto)
        self.frame_delay_time = QtWidgets.QFrame(widget_chapterList)
        self.frame_delay_time.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_delay_time.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_delay_time.setObjectName("frame_delay_time")
        self.hlay_delay_time = QtWidgets.QHBoxLayout(self.frame_delay_time)
        self.hlay_delay_time.setContentsMargins(11, 0, 11, 0)
        self.hlay_delay_time.setSpacing(7)
        self.hlay_delay_time.setObjectName("hlay_delay_time")
        self.spinBox_delay_time = QtWidgets.QSpinBox(self.frame_delay_time)
        self.spinBox_delay_time.setMinimumSize(QtCore.QSize(80, 0))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        self.spinBox_delay_time.setFont(font)
        self.spinBox_delay_time.setMinimum(1)
        self.spinBox_delay_time.setProperty("value", 5)
        self.spinBox_delay_time.setObjectName("spinBox_delay_time")
        self.hlay_delay_time.addWidget(self.spinBox_delay_time)
        self.label_delay_time = QtWidgets.QLabel(self.frame_delay_time)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        self.label_delay_time.setFont(font)
        self.label_delay_time.setObjectName("label_delay_time")
        self.hlay_delay_time.addWidget(self.label_delay_time)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hlay_delay_time.addItem(spacerItem)
        self.verticalLayout.addWidget(self.frame_delay_time)
        self.frame_btn = QtWidgets.QFrame(widget_chapterList)
        self.frame_btn.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_btn.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_btn.setObjectName("frame_btn")
        self.hlay_btn = QtWidgets.QHBoxLayout(self.frame_btn)
        self.hlay_btn.setContentsMargins(0, 0, 0, 0)
        self.hlay_btn.setSpacing(0)
        self.hlay_btn.setObjectName("hlay_btn")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hlay_btn.addItem(spacerItem1)
        self.btn_ok = QtWidgets.QPushButton(self.frame_btn)
        self.btn_ok.setObjectName("btn_ok")
        self.hlay_btn.addWidget(self.btn_ok)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hlay_btn.addItem(spacerItem2)
        self.btn_cancle = QtWidgets.QPushButton(self.frame_btn)
        self.btn_cancle.setObjectName("btn_cancle")
        self.hlay_btn.addWidget(self.btn_cancle)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hlay_btn.addItem(spacerItem3)
        self.verticalLayout.addWidget(self.frame_btn)

        self.retranslateUi(widget_chapterList)
        QtCore.QMetaObject.connectSlotsByName(widget_chapterList)

    def retranslateUi(self, widget_chapterList):
        _translate = QtCore.QCoreApplication.translate
        widget_chapterList.setWindowTitle(_translate("widget_chapterList", "章节"))
        self.checkBox_all_check.setText(_translate("widget_chapterList", "全选"))
        self.checkBox_check_auto.setText(_translate("widget_chapterList", "自动修复内容为空的章节"))
        self.label_delay_time.setText(_translate("widget_chapterList", "修复每章的延迟时间"))
        self.btn_ok.setText(_translate("widget_chapterList", "确定"))
        self.btn_cancle.setText(_translate("widget_chapterList", "取消"))

