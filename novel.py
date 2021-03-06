# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication, QWidget, QAction, QMenu, QSizePolicy, QSpacerItem, \
    QFileDialog, QFrame, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QProgressBar, QLineEdit, \
    QDialog, QListWidgetItem, QGraphicsOpacityEffect, QRadioButton, \
    QComboBox, QCompleter, QCheckBox, QHeaderView, QTableWidgetItem
from PyQt5.QtCore import Qt, QThread, QSize, QPropertyAnimation, QEasingCurve, \
    qInstallMessageHandler, QModelIndex, QFileInfo, QPoint, pyqtSlot
from PyQt5.Qt import QCursor, QMovie, QSystemTrayIcon, QRect
from PyQt5.QtGui import QTextDocument, QFont, QIcon, QPalette, QPixmap, QMouseEvent, \
    QTextCursor, QFontMetrics, QBrush, QColor

from datetime import datetime
from debug import QThread_Debug
from novel_glob import novel_init as global_init, set_value as global_set_value, get_value as global_get_value
from highlighter import UserRuleHighLight
from readWebView import ReadWindow
from Resource import novel_rc
from time import time as time_time
from ui.novel import Ui_Novel
from QDialog_ReadNetJson import QDialog_ReadNetJson
from QFrame_BookShelfImage import QFrame_BookShelfImage
from QLabel_playSound import QLabel_playSound
from QMenu_DebugUserRule import QMenu_DebugUserRule
from QMessageBox_showMsg import QMessageBox_showMsg
from QPushButton_BookShelf import QPushButton_BookShelf
from QPushButton_changeHoverIcon import QPushButton_changeHoverIcon
from Qss import Qss
from QTextEdit_response_preview import QTextEdit_response_preview
from QThread_AddNewRule import QThread_AddNewRule
from QThread_AddNewPurify import QThread_AddNewPurify
from QThread_Calculate_Cache_Size import QThread_Calculate_Cache_Size
from QThread_Clear_Cache import QThread_Clear_Cache
from QThread_DeleteUserLocalSQL import QThread_DeleteUserLocalSQL
from QThread_DeleteUserJsonRule import QThread_DeleteUserJsonRule
from QThread_DeleteUserPurifyJsonRule import QThread_DeleteUserPurifyJsonRule
from QThread_Download import QThread_Download
from QThread_ReadNetRule import QThread_ReadNetRule
from QThread_PurifyReadNetRule import QThread_PurifyReadNetRule
from QThread_SaveNewRule import QThread_SaveNewRule
from QThread_SaveNewPurifyRule import QThread_SaveNewPurifyRule
from QThread_Search import QThread_Search
from QThread_SelectLocalSQLDatabase import QThread_SelectLocalSQLDatabase
from QThread_UserData import QThread_UserData, threadUpdateUserSQLLeftWidget
from QThread_UpdateLatestChapter import QThread_UpdateLatestChapter
from QThread_RepairBookChapter import QThread_RepairBookChapter
from QThread_UpdateUserRuleEnable import QThread_UpdateUserRuleEnable, QThread_UpdatePurifyRuleEnable
from QThread_Xpath import QThread_Xpath
from QThread_Xpath_parse_one import QThread_Xpath_parse_one
from QThread_Xpath_parse_two import QThread_Xpath_parse_two
from QThread_ReadRule import QThread_ReadRule
from QThread_ReadPurifyRule import QThread_ReadPurifyRule
from QWidget_BookIntroduction import QWidget_BookIntroduction
from QWidget_Mask_Update_chapter import QWidget_Mask_Update_chapter
from QWidget_chapterList import QWidget_chapterList

import sys
import os
import re
import User
import regular
import purify
import atexit
import signal
from log import Logger

log = Logger().getlog()
main_pid = os.getpid()


class Window(QWidget, Ui_Novel):  # ??????????????????
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        global_init()  # ??????????????????
        self.bookShelfLayoutNums = -1  # ???????????????????????????
        self.downloadLayoutNums = -1  # ??????????????????????????????
        self.responseHTMl = ""  # ????????????????????????html??????
        local_json = regular.Json()
        self.rule = local_json.getData()  # ????????????????????????
        self.purify_rule = purify.Json().getData()  # ??????????????????????????????
        self.checkSQLImagePath()  # ????????????????????????????????????
        self.setEvent()  # ??????????????????
        self.extraSetting()  # ???????????????
        self.extraCursorSetting()  # ???????????????????????????
        self.extraPromptControlLayout()  # ?????????????????????
        self.extraTiplayout()  # ?????????????????????2
        self.setStyleSheet(Qss.readQss(QFileInfo("./Resource/novel.qss").absoluteFilePath()))
        self.initUserRuleLayout()  # ??????????????????????????????????????????rule??????
        self.initPurifyRuleLayout()  # ????????????????????????????????????????????????rule??????
        self.initAddNoneSearch()  # ????????????????????????????????????
        self.initSearchLoading()  # ???????????????gif
        self.initAddNoBookShelf()  # ?????????????????????????????????
        self.initAddBookShelf()  # ????????????????????????
        self.initAddLineEditSearchBtn()  # ????????????????????????????????????????????????
        self.initNoDownloadRecording()  # ????????????????????????
        self.initDownloadRecording()  # ?????????????????????
        self.initAddLabelSearchLoadingRefresh()  # ???????????????????????????????????????
        self.initAddResponse()  # ?????????????????????url???response text???textedit??????
        self.initXpathSetting()  # ?????????Xpath??????????????????
        self.initManageLocalSQLLayout()  # ????????????????????????
        self.initCompleter()  # ???????????????????????????
        self.initCacheImagesEvent()  # ???????????? ????????????????????????????????????
        self.m_flag = None  # ????????????
        self.retrieveDataTamperingStatus = 0  # ??????????????????????????? ??????0?????????

    def addBookShelfBook(self, bookImage, bookName, bookProgress, bookNums, serialNumber) -> None:  # ????????????????????????
        log.info(f"??????????????????{self.bookShelfLayoutNums + 1}")
        frame_line = self.findChildren(QFrame, 'frame_bookshelf_line')  # ???frame
        current_book_shelf_book_nums = self.bookShelfLayoutNums + 1
        if current_book_shelf_book_nums == 0:  # ????????????????????????????????????
            log.info("????????????????????????????????????")
            hlayout_bookshelf_line = self.addNewHlayoutLine()
            frame_book = self.addFrameBook(bookName=bookName,
                                           bookReadProgress=bookProgress,
                                           bookNums=bookNums,
                                           bookImagePath=bookImage,
                                           serialNumber=serialNumber
                                           )
            hlayout_bookshelf_line.addWidget(frame_book)
            self.frame_noneBookShelf.hide()

        elif current_book_shelf_book_nums % 4 == 0:  # ??????4??????????????????????????????????????????
            log.info("???????????????????????????")
            hlayout_bookshelf_line = self.addNewHlayoutLine()
            frame_book = self.addFrameBook(bookName=bookName,
                                           bookReadProgress=bookProgress,
                                           bookNums=bookNums,
                                           bookImagePath=bookImage,
                                           serialNumber=serialNumber
                                           )
            hlayout_bookshelf_line.addWidget(frame_book)
            # hSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            # hlayout_bookshelf_line.addItem(hSpacer)
        else:  # ?????????????????????????????????
            log.info("?????????????????????????????????")
            current_frame_line: QFrame = frame_line[-1]
            current_frame_line_hlayout: QHBoxLayout = current_frame_line.findChild(QHBoxLayout,
                                                                                   "hlayout_bookshelf_line")
            current_frame_line_frameindex = len(current_frame_line.findChildren(QFrame, "frame_book"))
            frame_book = self.addFrameBook(bookName=bookName,
                                           bookReadProgress=bookProgress,
                                           bookNums=bookNums,
                                           bookImagePath=bookImage,
                                           serialNumber=serialNumber
                                           )
            current_frame_line_hlayout.insertWidget(current_frame_line_frameindex, frame_book)
        self.bookShelfLayoutNums += 1
        log.info("????????????????????????")

    def addFrameBook(self, bookName: str,
                     bookReadProgress: float,
                     bookNums: int,
                     bookImagePath: str,
                     serialNumber: int) -> QFrame:  # ?????????frame
        frame_book = QFrame()  # ???frame
        frame_book.setObjectName("frame_book")
        frame_image = QFrame_BookShelfImage(self.bookShelfLayoutNums, self.frame_noneBookShelf)  # ??????frame
        frame_image.setProperty("updating", "0")
        frame_image.setProperty("repairing", "0")
        frame_image.setProperty("serialNumber", serialNumber)
        frame_image.setProperty("frame_image_mask", None)
        frame_image.breakSignal_bookinfo_frame.connect(self.call_showBookInfo)
        frame_image.breakSignal_bookinfo_update_chapter.connect(self.call_update_chapter)
        frame_image.breakSignal_bookinfo_update_bookShelfLayout.connect(self.call_updateBookShelfLayout)
        frame_image.breakSignal_bookinfo_repair_chapter.connect(self.call_showBookChapterList)
        frame_image.breakSignal_bookinfo_lessBookNums.connect(self.call_lessBookShelfNums)
        frame_image.breakSignal_delBookInDownloadLayout.connect(self.call_delBookInDownloadLayout)

        vlayout_book = QVBoxLayout()  # ?????????
        vlayout_image = QVBoxLayout()  # ????????????
        btn_image = QPushButton_BookShelf()
        btn_image.breakSignal_showReader.connect(self.call_showReader)
        label_book_name = QLabel()
        label_name_metrics = QFontMetrics(QFont("Microsoft YaHei", 11))
        label_book_name.setText(label_name_metrics.elidedText(bookName, Qt.ElideRight, 110))
        label_book_progress = QLabel(f"??????:{bookReadProgress}%")

        frame_image.setLabelObject(label_book_progress)

        btn_image.setMinimumSize(100, 150)
        btn_image.setMaximumSize(100, 150)

        btn_image.setObjectName(f"btn_bookshelf_image_{bookNums}")
        btn_image.setStyleSheet(f'''
                        border-image:url("{bookImagePath}");
                        border:none;
                        ''')
        label_book_name.setFont(QFont("Microsoft YaHei", 11))
        label_book_name.setAlignment(Qt.AlignCenter)
        label_book_progress.setFont(QFont("Microsoft YaHei", 9, QFont.Bold))
        label_book_progress.setStyleSheet("color:#b2b2b2")
        label_book_progress.setAlignment(Qt.AlignCenter)
        label_book_name.setContentsMargins(0, 0, 0, 0)
        label_book_progress.setContentsMargins(0, 0, 0, 0)
        vlayout_book.setAlignment(Qt.AlignCenter)
        vlayout_book.setContentsMargins(0, 0, 0, 0)
        vlayout_image.addWidget(btn_image)
        frame_image.setLayout(vlayout_image)
        vlayout_image.setContentsMargins(0, 0, 0, 0)
        frame_image.setContentsMargins(1, 1, 1, 1)
        frame_image.setStyleSheet(
            "border-radius: 6px;"
            "border:2px solid #b2b2b2;"
        )
        vlayout_book.addWidget(frame_image)
        vlayout_book.addWidget(label_book_name)
        vlayout_book.addWidget(label_book_progress)
        frame_book.setContentsMargins(0, 0, 0, 0)
        frame_book.setLayout(vlayout_book)
        frame_image.setContextMenuPolicy(Qt.CustomContextMenu)
        # frame_image.setContextMenuPolicy(3)
        frame_image.setMinimumSize(105, 155)
        frame_image.setMaximumSize(105, 155)
        frame_book.setMinimumSize(125, 250)
        frame_book.setMaximumSize(125, 250)
        log.info(f"???????????????{frame_book}")
        return frame_book

    def addNewRuleLayout(self, bookSourceName: str, enable: bool):
        item = QListWidgetItem()
        item.setTextAlignment(Qt.AlignLeft)
        item.setSizeHint(QSize(200, 50))
        item_widget = QFrame()
        item_widget.setObjectName("frame_rule_item_widget")
        item_widget.setStyleSheet("background-color: transparent;")
        item_widget_layout = QHBoxLayout()
        leftCheckBox = QCheckBox()
        leftCheckBox.setObjectName("rule_leftCheckBox")
        chooseBox = QCheckBox()
        chooseBox.setProperty("QListWidgetItem", item)
        chooseBox.setChecked(True if enable else False)
        chooseBox.stateChanged.connect(self.on_rule_choose_item_stateChanged)
        label_rulename = QLabel()
        label_rulename.setFont(QFont("Microsoft YaHei", 9))
        label_rulename.setObjectName("label_rule_item_widget")
        label_rulename.setMaximumWidth(106)
        label_rulename_metrics = QFontMetrics(QFont("Microsoft YaHei", 9))
        label_rulename.setText(
            label_rulename_metrics.elidedText(bookSourceName, Qt.ElideRight, label_rulename.maximumWidth()))
        chooseBox.setObjectName("checkbox_enable")
        label_rulename.setStyleSheet("background-color: transparent;")
        item_widget_layout.addWidget(leftCheckBox)
        item_widget_layout.addWidget(label_rulename)
        item_widget_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        item_widget_layout.addWidget(chooseBox)
        item_widget.setLayout(item_widget_layout)

        self.listWidget_rule_userRule.addItem(item)
        self.listWidget_rule_userRule.setItemWidget(item, item_widget)
        self.update()

    def addNewPurifyLayout(self, purifySourceName: str, enable: bool):
        item = QListWidgetItem()
        item.setTextAlignment(Qt.AlignLeft)
        item.setSizeHint(QSize(200, 50))
        item_widget = QFrame()
        item_widget.setObjectName("frame_purify_rule_item_widget")
        item_widget.setStyleSheet("background-color: transparent;")
        item_widget_layout = QHBoxLayout()
        leftCheckBox = QCheckBox()
        leftCheckBox.setObjectName("purify_rule_leftCheckBox")
        chooseBox = QCheckBox()
        chooseBox.setProperty("QListWidgetItem_purify", item)
        chooseBox.setChecked(True if enable else False)
        chooseBox.stateChanged.connect(self.on_purify_choose_item_stateChanged)
        label_rulename = QLabel()
        label_rulename.setFont(QFont("Microsoft YaHei", 9))
        label_rulename.setObjectName("label_rule_item_widget")
        label_rulename.setMaximumWidth(106)
        label_rulename_metrics = QFontMetrics(QFont("Microsoft YaHei", 9))
        label_rulename.setText(
            label_rulename_metrics.elidedText(purifySourceName, Qt.ElideRight, label_rulename.maximumWidth()))
        chooseBox.setObjectName("checkbox_enable")
        label_rulename.setStyleSheet("background-color: transparent;")
        item_widget_layout.addWidget(leftCheckBox)
        item_widget_layout.addWidget(label_rulename)
        item_widget_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        item_widget_layout.addWidget(chooseBox)
        item_widget.setLayout(item_widget_layout)

        self.listWidget_purify.addItem(item)
        self.listWidget_purify.setItemWidget(item, item_widget)
        self.update()

    def addNewHlayoutLine(self) -> QHBoxLayout:  # ????????????hlayout
        frame_bookshelf_line = QFrame()  # ???frame
        frame_bookshelf_line.setObjectName("frame_bookshelf_line")
        hlayout_bookshelf_line = QHBoxLayout()  # ?????????
        hlayout_bookshelf_line.setObjectName("hlayout_bookshelf_line")

        hlayout_bookshelf_line.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        hlayout_bookshelf_line.setSpacing(120)
        frame_bookshelf_line.setContentsMargins(60, 0, 1260, 0)
        frame_bookshelf_line.setLayout(hlayout_bookshelf_line)

        self.vlayout_bookshelf_top.addWidget(frame_bookshelf_line)

        return hlayout_bookshelf_line

    def btnReadEvent(self,
                     bookImage: str,
                     bookName: str,
                     bookProgress: float,
                     bookPath: str,
                     bookAuthor: str,
                     bookStatus: str,
                     bookLatestChapter: str,
                     bookLatestUpdateTime: str,
                     bookIntro: str,

                     bookSourceName: str,
                     bookUrl: str,
                     bookRule: int,
                     bookSerialNumber: int
                     ) -> None:
        # ???????????????????????????
        # ??????????????????
        # ????????????????????????????????????????????????0?????????????????????????????????(????????????????????????????????????+1)??????????????????????????????,?????????????????????????????????????????????
        # ?????????????????????????????????????????????(url),????????????????????????
        user = User.UserSql()
        total_nums = user.selectBookShelfChapterTotalNums(serialNumer=bookSerialNumber)[0]
        log.info(str(total_nums))
        if total_nums:
            self.insertBookShelfLayoutInfoSqlite(
                bookImage=bookImage,
                bookName=bookName,
                bookProgress=bookProgress,
                bookPath=bookPath,
                bookAuthor=bookAuthor,

                bookStatus=bookStatus,
                bookLatestChapter=bookLatestChapter,
                bookLatestUpdateTime=bookLatestUpdateTime,
                bookIntro=bookIntro,
                bookSourceName=bookSourceName,

                bookUrl=bookUrl,
                bookRule=bookRule,
                bookSerialNumber=bookSerialNumber
            )
            # ??????????????????????????????????????????
            self.insertReaderBookNormalInfo(currentPage=1,
                                            serialNumber=bookSerialNumber,
                                            scrollTop=0)
        else:
            QMessageBox_showMsg(title="??????????????????", text="?????????????????????????????????????????????????????????").makeSure()

    def btnSaveRule(self) -> None:  # ?????????????????????rule
        log.info("??????rule")
        selectIndex = self.btn_rule_save.property("now_row")
        self.thread_saveNewRule = QThread_SaveNewRule(selectIndex=selectIndex,
                                                      lineEdit_every_text=self.getJsonRuleDictObjectText())
        self.thread_saveNewRule.breakSignal_isSuccess.connect(self.call_getUpdateUserRuleStatus)
        self.thread_saveNewRule.start()

    def btnPurifySaveRule(self) -> None:  # ???????????????????????????rule
        log.info("????????????rule")
        selectIndex = self.btn_purify_save.property("now_row")
        self.thread_saveNewPurifyRule = QThread_SaveNewPurifyRule(
            selectIndex=selectIndex,
            lineEdit_every_text=self.getPurifyJsonRuleDictObjectText())
        self.thread_saveNewPurifyRule.breakSignal_isSuccess.connect(self.call_getUpdateUserPurifyRuleStatus)
        self.thread_saveNewPurifyRule.start()

    @staticmethod
    def btnFileEvent(filePath: str, fileName: str) -> None:
        fileNewPath = filePath.replace("/", "\\") + "\\" + fileName + ".txt"
        log.info(f"?????????????????????{fileNewPath}")
        if os.path.isfile(fileNewPath):
            os.system(f"explorer /select,{fileNewPath}")
        else:
            os.startfile(filePath)

    def btnReadNetJson(self, obj: QDialog) -> None:
        net_json = obj.lineEdit.text()
        net_json_match = re.findall(r'http(s|)://.+.json', net_json, re.S)
        if net_json_match:
            obj.close()
            self.thread_readNetRule = QThread_ReadNetRule(netJsonLink=net_json)
            self.thread_readNetRule.breakSignal_updateRuleLayout.connect(self.call_updateRuleLayout)
            self.thread_readNetRule.run()
        elif net_json == "":
            QMessageBox_showMsg(title="??????", text="???????????????!", Windows=self).makeSure()
            log.info("??????????????????")
        elif net_json.strip() == "":
            QMessageBox_showMsg(title="????????????", text="??????????????????", Windows=self).makeSure()
            log.info("??????????????????")
        else:
            QMessageBox_showMsg(title="????????????", text="???????????????json??????!", Windows=self).makeSure()
            log.info("??????????????????json??????")

    def btnPurifyReadNetJson(self, obj: QDialog):
        net_json = obj.lineEdit.text()
        net_json_match = re.findall(r'http(s|)://.+.json', net_json, re.S)
        if net_json_match:
            obj.close()
            self.thread_purifyReadNetRule = QThread_PurifyReadNetRule(netJsonLink=net_json)
            self.thread_purifyReadNetRule.breakSignal_updatePurifyRuleLayout.connect(self.call_updatePurifyRuleLayout)
            self.thread_purifyReadNetRule.run()
        elif net_json == "":
            QMessageBox_showMsg(title="??????", text="???????????????!", Windows=self).makeSure()
            log.info("??????????????????")
        elif net_json.strip() == "":
            QMessageBox_showMsg(title="????????????", text="??????????????????", Windows=self).makeSure()
            log.info("??????????????????")
        else:
            QMessageBox_showMsg(title="????????????", text="???????????????json??????!", Windows=self).makeSure()
            log.info("??????????????????json??????")

    def btnDelEvent(self, row: int, widget: QWidget) -> None:
        makesure = QMessageBox_showMsg(text="????????????????????????????", icon="").makeSures()
        if makesure:
            number_of_download_tasks_now = global_get_value(key="number_of_download_tasks_now")
            number_of_download_tasks_now -= 1
            global_set_value(key="number_of_download_tasks_now", value=number_of_download_tasks_now)
            # nowDownloadNums -= 1
            log.info(f"??????????????????{row}")
            user = User.UserSql()
            user.deleteDownloadLayoutInfo(row)
            widget.deleteLater()
            self.downloadLayoutNums -= 1
            log.info(f"????????????????????????????????????{self.downloadLayoutNums}")
            if self.downloadLayoutNums == -1:
                self.frame_noDownload.show()

    def checkSQLImagePath(self):
        log.info("????????????????????????????????????")
        user = User.UserSql()
        selectImagePath_bookshelf = user.selectBookShelfImagePath()
        selectImagePath_download = user.selectDownloadImagePath()
        for select_bookshelf in selectImagePath_bookshelf:
            image_path: list = select_bookshelf[0].split("/")
            serial_number = select_bookshelf[1]
            image_name = image_path[-1]
            image_old_path = "/".join(image_path[:-1])
            current_path_cache = QFileInfo("./Resource/Cache").absoluteFilePath()
            current_path_noCover = QFileInfo("./Resource").absoluteFilePath()
            if image_name == "noCover.jpeg":
                if image_old_path != current_path_noCover:
                    new_imag_path = f"{current_path_noCover}/noCover.jpeg"
                    log.info(f"noCover????????????????????????:{image_old_path}/{image_name}????????????:{new_imag_path}????????????:bookshelf")
                    user.updateBookShelfImagePath(imagePath=new_imag_path, serialNumber=serial_number)
            else:
                if image_old_path != current_path_cache:
                    new_imag_path = f"{current_path_cache}/{image_name}"
                    log.info(f"????????????????????????????????????:{image_old_path}/{image_name}????????????:{new_imag_path}????????????:bookshelf")
                    user.updateBookShelfImagePath(imagePath=new_imag_path, serialNumber=serial_number)

        for select_download in selectImagePath_download:
            image_path: list = select_download[0].split("/")
            serial_number = select_download[1]
            image_name = image_path[-1]
            image_old_path = "/".join(image_path[:-1])
            current_path_cache = QFileInfo("./Resource/Cache").absoluteFilePath()
            current_path_noCover = QFileInfo("./Resource").absoluteFilePath()
            if image_name == "noCover.jpeg":
                if image_old_path != current_path_noCover:
                    new_imag_path = f"{current_path_noCover}/noCover.jpeg"
                    log.info(f"noCover????????????????????????:{image_old_path}/{image_name}????????????:{new_imag_path}????????????:download")
                    user.updateDownloadImagePath(imagePath=new_imag_path, serialNumber=serial_number)
            else:
                if image_old_path != current_path_cache:
                    new_imag_path = f"{current_path_cache}/{image_name}"
                    log.info(f"????????????????????????????????????:{image_old_path}/{image_name}????????????:{new_imag_path}????????????:download")
                    user.updateDownloadImagePath(imagePath=new_imag_path, serialNumber=serial_number)

    def call_getUpdateUserRuleStatus(self, bookSourceName: str):
        log.info("??????????????????rule??????,????????????????????????")
        self.update_self_rule()
        select_index = self.btn_rule_save.property("now_row")
        choose_item = self.listWidget_rule_userRule.item(select_index)
        choose_item_widget = self.listWidget_rule_userRule.itemWidget(choose_item)
        choose_item_widget_label = choose_item_widget.findChild(QLabel)
        if choose_item_widget_label:
            log.info(f"?????????:{choose_item_widget_label.text()}")
            label_rulename_metrics = QFontMetrics(QFont("Microsoft YaHei", 9))
            choose_item_widget_label.setText(
                label_rulename_metrics.elidedText(bookSourceName, Qt.ElideRight,
                                                  choose_item_widget_label.maximumWidth()))
            log.info(f"?????????:{choose_item_widget_label.text()}")

    def call_getUpdateUserPurifyRuleStatus(self, purifySourceName: str):
        log.info("????????????????????????rule??????,????????????????????????")
        self.update_self_purify_rule()
        select_index = self.btn_purify_save.property("now_row")
        choose_item = self.listWidget_purify.item(select_index)
        choose_item_widget = self.listWidget_purify.itemWidget(choose_item)
        choose_item_widget_label = choose_item_widget.findChild(QLabel)
        if choose_item_widget_label:
            log.info(f"?????????:{choose_item_widget_label.text()}")
            label_rulename_metrics = QFontMetrics(QFont("Microsoft YaHei", 9))
            choose_item_widget_label.setText(
                label_rulename_metrics.elidedText(purifySourceName, Qt.ElideRight,
                                                  choose_item_widget_label.maximumWidth()))
            log.info(f"?????????:{choose_item_widget_label.text()}")

    def call_updateRuleLayout(self, s):  # ??????????????????????????????
        log.info(f"??????????????????{s}")
        # ??????????????????
        for i in range(self.listWidget_rule_userRule.count()):
            log.info(f"?????????{i}???")
            self.listWidget_rule_userRule.takeItem(0)
        self.update_self_rule()
        self.initUserRuleLayout()

    def call_updatePurifyRuleLayout(self, s):  # ????????????????????????????????????
        log.info(f"????????????????????????{s}")
        for i in range(self.listWidget_purify.count()):
            log.info(f"?????????{i}???")
            self.listWidget_purify.takeItem(0)
        self.update_self_purify_rule()
        self.initPurifyRuleLayout()

    def changeBtnFont(self, args) -> None:  # ????????????????????????
        obj = [self.frame_main_down_getbook_small,
               self.frame_main_down_bookshelf, self.frame_main_down_bookshelf_small,
               self.frame_main_down_download, self.frame_main_down_download_small,
               self.frame_main_down_rule, self.frame_main_down_rule_small,
               self.frame_main_down_xpath, self.frame_main_down_xpath_small,
               self.frame_main_down_setting, self.frame_main_down_setting_small,
               self.frame_main_down_manage, self.frame_main_down_manage_small
               ]
        for i in obj:
            if i.objectName() in args:
                i.setStyleSheet("border-left:5px solid rgba(0, 90, 158,1);")
            else:
                i.setStyleSheet("border-left:5px solid transparent;")

    def call_addSearchResult(self,
                             imagePath: str,
                             bookname: str,
                             bookIntro: str,
                             homeurl: str,
                             whichRule: int,
                             bookAuthor: str,
                             bookStatus: str,
                             bookSourceName: str,
                             bookLatestChapter: str,
                             bookLatestUpdateTime: str,
                             bookIntroduction: str,
                             bookname_similarity: float,  # ???????????????
                             author_similarity: float,  # ??????????????????
                             combobox_index: int,  # ?????????????????????
                             isDownload: int
                             ) -> None:  # ???????????????????????? ?????? ?????????????????? ???N?????????
        # if (len(bookIntro) > 320):
        #     bookIntro = bookIntro[0:320] + "......"\
        # ???????????????????????????
        # ????????????
        frame = QFrame()
        btn_image = QPushButton()
        btn_download = QPushButton()
        label_instruction = QLabel()
        h_layout = QHBoxLayout()

        frame.setFrameShape(QFrame.StyledPanel)
        frame.setFrameShadow(QFrame.Raised)
        frame.setObjectName("searchResultListFrame")

        # ??????????????????
        label_instruction.setMinimumSize(480, 200)
        label_instruction.setMaximumSize(480, 200)
        label_instruction.setText(bookIntro)
        label_instruction.setStyleSheet(" font-family: Microsoft YaHei; font-size: 14px;")
        label_instruction.setAlignment(Qt.AlignLeft)
        label_instruction.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        label_instruction.setWordWrap(True)

        font = QFont()
        font.setFamily("Microsoft YaHei")
        icon = QIcon()
        icon.addPixmap(QPixmap(QFileInfo("./Resource/icon/d_128.png").absoluteFilePath()), QIcon.Normal, QIcon.Off)

        btn_image.setMinimumSize(QSize(150, 200))
        btn_image.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        btn_image.setStyleSheet('''
        QPushButton{
            border-image:url("%s");
            border-radius: 6px;
        }
        ''' % imagePath)
        btn_download.setText("????????????")
        btn_download.setObjectName("btn_searchResult_toDownload")
        btn_download.setStyleSheet('''
        QPushButton:disabled{
            color:rgb(182, 182, 182);
        }
        ''')
        btn_download.setMinimumSize(131, 41)
        btn_download.setMaximumSize(131, 41)
        btn_download.setFont(font)
        btn_download.setIcon(icon)
        btn_download.setCursor(QCursor(QPixmap(QFileInfo(":/cursor/Cur/work.cur").absoluteFilePath()), 0, 0))
        # ?????? ????????????????????????????????????????????????????????????rule
        # btn_download.clicked.connect(lambda: self.call_addDownloadLayout(imagePath,homeurl, whichRule)) #????????????????????????
        btn_download.clicked.connect(self.hideNoDownload)  # ????????????????????????frame???????????????
        btn_download.clicked.connect(
            lambda: self.call_addDownloadLayout(
                bookname=bookname,
                bookAuthor=bookAuthor,
                bookStatus=bookStatus,
                bookIntro=bookIntroduction,
                bookSourceName=bookSourceName,
                bookLatestChapter=bookLatestChapter,
                bookLatestUpdateTime=bookLatestUpdateTime,
                imagePath=imagePath,
                homeurl=homeurl,
                whichRule=whichRule
            ))  # ????????????????????????

        tip_info = f"???: ???{bookname}???"
        btn_download.clicked.connect(lambda: self.extraPromptControlLayoutAnimation(tip_info))  # ????????????????????????????????????

        h_layout.addWidget(btn_image, 0, Qt.AlignLeft)
        h_layout.addWidget(label_instruction, 0, Qt.AlignLeft)
        h_layout.addWidget(btn_download, 0, Qt.AlignRight | Qt.AlignVCenter)
        h_layout.setAlignment(Qt.AlignTop)

        frame.setLayout(h_layout)

        frame.setProperty("bookname_similarity", bookname_similarity)
        frame.setProperty("author_similarity", author_similarity)
        if isDownload:
            btn_download.setText("?????????")
            btn_download.setEnabled(False)

        insert_index = self.getSearchResultInsertIndex(sort_choose=combobox_index,
                                                       this_similarity=bookname_similarity,
                                                       that_property_key="bookname_similarity")
        if insert_index is None:
            self.vlayout_search_result_scrollAreaWidgetContents.addWidget(frame)
        else:
            log.info(f"????????????{insert_index}")
            self.vlayout_search_result_scrollAreaWidgetContents.insertWidget(insert_index, frame)
        log.info(f"?????????????????????{bookname}")

    def call_appendResultText(self, s):
        self.textEdit_getUrl_getResult_response.append(s)

    def call_insertResultHTML(self, s):
        self.textEdit_getUrl_getResult_preview.setUpdatesEnabled(False)
        self.textEdit_getUrl_getResult_preview.insertHtml(s)
        self.textEdit_getUrl_getResult_preview.setUpdatesEnabled(True)

    def call_appendTestXpathText(self, s):
        self.textEdit_testXpath_getResult.append(s)

    def call_insertTestXpathHTML(self, s):
        self.textEdit_testXpath_getResult.insertHtml(s)

    def call_addSearchResultShowNoneSearch(self) -> None:  # ?????????????????????
        self.label_noneSearch.setText(f'????????????"{self.lineEdit_search.text()}" ???????????????!')
        self.frame_noneSearch.show()

    def call_addSearchResultShowSearchNums(self, s: str) -> None:  # ??????????????????????????????
        self.label_searchNum.setText(s)

    def call_addSearchResultHideLodingGif(self) -> None:  # ??????gif
        self.loding_movie.stop()
        self.frame_loding.hide()

    def call_addSearchResultHideReflushIcon(self) -> None:  # ????????????????????????
        self.label_refresh.hide()

    def call_addDownloadLayout(self,
                               bookname: str,  # ??????
                               bookAuthor: str,  # ?????????
                               imagePath: str,  # ??????????????????
                               homeurl: str,  # ????????????url
                               whichRule: int,  # ???????????????
                               bookStatus: str,  # ????????????
                               bookIntro: str,  # ??????
                               bookSourceName: str,  # ?????????
                               bookLatestChapter: str,  # ????????????
                               bookLatestUpdateTime: str,  # ????????????
                               isTaskSerialNumber: int = None,  # ??????
                               taskCreatTime: str = None,  # ??????????????????
                               taskFinishTime: str = None,  # ??????????????????
                               taskProgress: int = 0,  # Progress??????value
                               taskProgressLabel: int = 0,  # Progress???????????????label???????????????
                               taskBtnStatus: int = 0,  # ?????????????????????
                               taskStatusInfo: str = "??????",  # ?????????...

                               task: bool = True  # ????????????????????????????????????????????????????????????????????????????????????
                               ) -> None:  # ??????????????????????????????

        try:
            self.downloadLayoutNums += 1
            downloadLayoutNums = self.downloadLayoutNums
            saveFilePath = self.lineEdit_setting_downloadLocation.text()
            bookFilePath = saveFilePath + f"/{bookname}.txt"
            widget = QWidget()
            frame_right = QFrame()
            frame_center = QFrame()
            frame_center_top = QFrame()
            frame_center_down = QFrame()
            Vlayout_right = QVBoxLayout()
            Vlayout_center = QVBoxLayout()
            Vlayout_center_top = QVBoxLayout()
            Hlayout = QHBoxLayout()
            Hlayout_center_down = QHBoxLayout()
            Hlayout_center_down_2 = QHBoxLayout()
            Vlayout_center_down = QVBoxLayout()
            btn_image = QPushButton()
            btnAddBookToBookShelf = QPushButton_changeHoverIcon()
            btn_file = QPushButton_changeHoverIcon()
            btn_delete = QPushButton_changeHoverIcon()
            probar = QProgressBar()
            lb_bookname = QLabel()
            lb_start = QLabel()
            lb_end = QLabel()
            lb_progress = QLabel()
            lb_progress_state = QLabel("?????????")
            lb_progress_state_ = QLabel(taskStatusInfo)
            lb_probar = QLabel(f"{taskProgressLabel}%")
            spacer_right = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            spacer_up = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
            spacer_down = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

            taskCreatTime = taskCreatTime if taskCreatTime else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # taskSerialNumber = int(time.time()) #???????????????
            if task:
                taskSerialNumber = int(time_time())  # ???????????????
            else:
                taskSerialNumber = isTaskSerialNumber
            taskFinishTime = taskFinishTime if taskFinishTime else "-??-"
            lb_bookname.setText(f"""<li>?????????
                                        <span>
                                            <font color="#F30">{bookname}</font>
                                        </span>
                                    </li>
                            """)
            lb_start.setText(f"???????????????{taskCreatTime}")
            lb_end.setText(f"???????????????{taskFinishTime}")
            lb_progress.setText("?????????")
            btnAddBookToBookShelf.setText("????????????")
            btn_file.setText("????????????")
            btn_delete.setText("????????????")
            btnAddBookToBookShelf.setCursor(QCursor(QPixmap(":/cursor/Cur/work.cur"), 0, 0))
            btn_file.setCursor(QCursor(QPixmap(":/cursor/Cur/work.cur"), 0, 0))
            btn_delete.setCursor(QCursor(QPixmap(":/cursor/Cur/work.cur"), 0, 0))

            btn_image.setMinimumSize(QSize(150, 200))
            btn_image.setStyleSheet(f'border-image:url("{imagePath}");border-radius: 6px;')
            btn_image.setAttribute(Qt.WA_TransparentForMouseEvents, True)

            lb_progress.setMinimumWidth(40)
            lb_progress.setMaximumWidth(40)
            lb_progress.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            probar.setValue(taskProgress)
            probar.setMinimumSize(QSize(190, 20))
            probar.setMaximumSize(QSize(190, 20))
            probar.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            lb_probar.setMinimumWidth(40)
            lb_probar.setMaximumWidth(40)
            lb_probar.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            lb_progress_state.setMinimumWidth(40)
            lb_progress_state.setMaximumWidth(40)
            lb_progress_state.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            lb_progress_state_.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            font = QFont()
            font.setFamily("Microsoft YaHei")
            btnAddBookToBookShelf.setFont(font)
            btn_file.setFont(font)
            btn_delete.setFont(font)

            btnAddBookToBookShelf.setObjectName("btn_downloadlayout_addtobook")
            btn_file.setObjectName("btn_downloadlayout_openfile")
            btn_delete.setObjectName("btn_downloadlayout_deletelayoutinfo")
            btnAddBookToBookShelf.setProperty("currentBtn", "add_to_bookshelf")
            btn_file.setProperty("currentBtn", "open_book_file")
            btn_delete.setProperty("currentBtn", "del_from_download_layout")

            btnAddBookToBookShelf.setIcon(QIcon(QFileInfo("./Resource/icon/addToBookShelf.png").absoluteFilePath()))
            btn_file.setIcon(QIcon(QFileInfo("./Resource/icon/file.png").absoluteFilePath()))
            btn_delete.setIcon(QIcon(QFileInfo("./Resource/icon/delete.png").absoluteFilePath()))

            btnAddBookToBookShelf.setMinimumSize(100, 30)
            btn_file.setMinimumSize(100, 30)
            btn_delete.setMinimumSize(100, 30)
            probar.setTextVisible(False)
            if not taskBtnStatus:
                btnAddBookToBookShelf.setEnabled(False)
                btn_file.setEnabled(False)
                # btn_delete.setEnabled(False)

            btnAddBookToBookShelf.clicked.connect(lambda: self.btnReadEvent(
                bookImage=imagePath,
                bookName=bookname,
                bookProgress=0,
                bookPath=bookFilePath,
                bookAuthor=bookAuthor,
                bookStatus=bookStatus,
                bookLatestChapter=bookLatestChapter,
                bookLatestUpdateTime=bookLatestUpdateTime,
                bookIntro=bookIntro,

                bookSourceName=bookSourceName,
                bookUrl=homeurl,
                bookRule=whichRule,
                bookSerialNumber=taskSerialNumber
            ))
            btn_file.clicked.connect(lambda: self.btnFileEvent(saveFilePath, bookname))
            btn_delete.clicked.connect(lambda: self.btnDelEvent(downloadLayoutNums, widget))

            # ????????????????????? frame_center
            # ????????????frame
            # =================================
            Vlayout_center_top.addWidget(lb_bookname)
            Vlayout_center_top.addWidget(lb_start)
            Vlayout_center_top.addWidget(lb_end)
            Vlayout_center_top.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            Vlayout_center_top.setContentsMargins(0, 0, 0, 0)
            frame_center_top.setLayout(Vlayout_center_top)

            # ????????????frame
            Hlayout_center_down.addWidget(lb_progress)
            Hlayout_center_down.addWidget(probar)
            Hlayout_center_down.addWidget(lb_probar)
            Hlayout_center_down.setAlignment(Qt.AlignBottom)
            Hlayout_center_down.setContentsMargins(0, 0, 0, 0)

            Hlayout_center_down_2.addWidget(lb_progress_state)
            Hlayout_center_down_2.addWidget(lb_progress_state_)
            Hlayout_center_down_2.setContentsMargins(0, 0, 0, 0)
            # frame_center_down.setLayout(Hlayout_center_down)
            Vlayout_center_down.addLayout(Hlayout_center_down)
            Vlayout_center_down.addLayout(Hlayout_center_down_2)
            Vlayout_center_down.setContentsMargins(0, 0, 0, 0)
            frame_center_down.setLayout(Vlayout_center_down)

            # ??????frame
            Vlayout_center.addWidget(frame_center_top)
            spacer_center = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
            Vlayout_center.addItem(spacer_center)
            Vlayout_center.addWidget(frame_center_down)
            Vlayout_center.setAlignment(Qt.AlignTop)
            frame_center.setContentsMargins(0, 0, 0, 0)
            frame_center.setLayout(Vlayout_center)
            # ====================================

            # ????????????????????? frame_right
            Vlayout_right.addWidget(btnAddBookToBookShelf)  # ??????
            Vlayout_right.addItem(spacer_up)  # ??????
            Vlayout_right.addWidget(btn_file)  # ??????
            Vlayout_right.addItem(spacer_down)  # ??????
            Vlayout_right.addWidget(btn_delete)  # ??????
            Vlayout_right.setAlignment(Qt.AlignRight | Qt.AlignTop)
            frame_right.setContentsMargins(0, 0, 0, 0)
            frame_right.setLayout(Vlayout_right)  # ?????????frame

            # ????????????????????? Hlayout
            Hlayout.addWidget(btn_image)  # ??????
            Hlayout.addWidget(frame_center)  # ?????????
            Hlayout.addItem(spacer_right)  # ??????
            Hlayout.addWidget(frame_right)  # ?????????
            Hlayout.setAlignment(Qt.AlignTop)

            widget.setLayout(Hlayout)
            self.vlayout_download_t.addWidget(widget)

            if task:
                self.insertDownloadLayoutInfoSqlite(taskBookImagePath=imagePath,
                                                    taskBookName=bookname,
                                                    taskCreateTime=taskCreatTime,
                                                    taskFinishTime=taskFinishTime,
                                                    taskProgress=taskProgress,
                                                    taskStatusInfo=taskStatusInfo,
                                                    taskBtnStatus=taskBtnStatus,
                                                    taskBookPath=bookFilePath,
                                                    taskLine=downloadLayoutNums,
                                                    taskHomeUrl=homeurl,
                                                    taskWhichRule=whichRule,
                                                    taskProgressLabel=taskProgressLabel,

                                                    taskBookAuthor=bookAuthor,
                                                    taskBookStatus=bookStatus,
                                                    taskBookIntro=bookIntro,
                                                    taskBookSourceName=bookSourceName,
                                                    taskBookLatestChapter=bookLatestChapter,
                                                    taskLatestUpdateTime=bookLatestUpdateTime,
                                                    taskSerialNumber=taskSerialNumber  # ???????????????
                                                    )  # ?????????????????????
                log.info(f"?????????????????????{bookname}")

                # ??????????????????????????????
                self.downloadThread = QThread_Download(probar=probar, bookname=bookname, lb_probar=lb_probar,
                                                       labelProgressState=lb_progress_state_,
                                                       btnAddBookToBookShelf=btnAddBookToBookShelf,
                                                       btnFile=btn_file, btnDel=btn_delete, lb_end=lb_end,
                                                       imagePath=imagePath, homeurl=homeurl,
                                                       taskSerialNumber=taskSerialNumber, whichRule=whichRule)

                self.downloadThread.start()
                downloadThread = self.downloadThread
                btn_delete.clicked.connect(lambda: self.deleteThreadDownloadTask(downloadThread))

            else:
                log.info(f"??????????????????{str(bookname)}")
        except Exception as err:
            log.error(err)

    def call_delBookInDownloadLayout(self, serialNumber: int, bookNums, status: int):
        log.info(f"????????????serialnumber:{serialNumber}")
        self.__thread_bookinfo = QThread_BookInfo(serialNumber=serialNumber, bookNums=bookNums)
        if status:
            self.__thread_bookinfo.setDelStatus(True)
        self.__thread_bookinfo.start()

    def call_getUpdateUserRuleEnableStatus(self, status: bool):
        log.info(f"????????????????????????:{str(status)}")
        self.update_self_rule()

    def call_getUpdatePurifyRuleEnableStatus(self, status: bool):
        log.info(f"????????????????????????:{str(status)}")
        self.update_self_purify_rule()

    def call_saveUserInfo(self, s: str) -> None:  # ????????????
        log.info(f"??????_??????????????????{s}")
        # ?????????????????????????????????????????????
        self.extraTiplayoutShow()

    def call_setUserRuleData(self, data: list):
        self.lineEdit_sourceName.setText(data[0])
        self.lineEdit_sourceUrl.setText(data[1])
        self.lineEdit_searchUrl.setText(data[2])
        self.lineEdit_charset.setText(data[3])
        if data[4] == 1:
            self.radioButton_get.setChecked(True)
        else:
            self.radioButton_post.setChecked(True)
        self.textEdit_data.setPlainText(data[5])
        self.lineEdit_searchList.setText(data[6])
        self.lineEdit_toUrl.setText(data[7])
        self.lineEdit_image.setText(data[8])
        self.lineEdit_bookName.setText(data[9])
        self.lineEdit_author.setText(data[10])
        self.lineEdit_endstate.setText(data[11])
        self.lineEdit_latestChapter.setText(data[12])
        self.lineEdit_updateTime.setText(data[13])
        self.lineEdit_introduction.setText(data[14])
        self.lineEdit_noneSearch.setText(data[15])
        self.lineEdit_text.setText(data[16])

    def call_setUserRuleDataModelOne(self, data: list):
        self.radioButton_model_1.setChecked(True)
        self.stackedWidget_rule_catalog.setCurrentIndex(0)
        self.lineEdit_model_1_element.setText(data[0])
        self.lineEdit_model_1_bookUrl.setText(data[1])
        self.lineEdit_model_1_bookName.setText(data[2])

    def call_setUserRuleDataModelTwo(self, data: list):
        self.radioButton_model_2.setChecked(True)
        self.stackedWidget_rule_catalog.setCurrentIndex(1)
        self.lineEdit_model_2_toUrl.setText(data[0])
        self.lineEdit_model_2_element.setText(data[1])
        self.lineEdit_model_2_bookUrl.setText(data[2])
        self.lineEdit_model_2_bookName.setText(data[3])

    def call_setUserRuleDataModelThree(self, data: list):
        self.radioButton_model_3.setChecked(True)
        self.stackedWidget_rule_catalog.setCurrentIndex(2)

    def call_setUserRuleDataModelFour(self, data: list):
        self.radioButton_model_4.setChecked(True)
        self.stackedWidget_rule_catalog.setCurrentIndex(3)
        self.lineEdit_model_4_toUrl.setText(data[0])
        self.lineEdit_model_4_element.setText(data[1])
        self.lineEdit_model_4_bookUrl.setText(data[2])
        self.lineEdit_model_4_bookName.setText(data[3])
        self.lineEdit_model_4_ajaxUrl.setText(data[4])
        if data[5] == 1:
            self.radioButton_model_4_ajaxMethod_get.setChecked(True)
        else:
            self.radioButton_model_4_ajaxMethod_post.setChecked(True)
        self.textEdit_model_4_ajaxData.setText(data[6])

    def call_setUserRuleDataModelFive(self, data: list):
        self.radioButton_model_5.setChecked(True)
        self.stackedWidget_rule_catalog.setCurrentIndex(4)
        self.lineEdit_model_5_nextPageUrl.setText(data[0])
        self.lineEdit_model_5_chapterElement.setText(data[1])
        self.lineEdit_model_5_chapterUrl.setText(data[2])
        self.lineEdit_model_5_chapterName.setText(data[3])

    def call_setUserRuleData_only_search(self, data: list):
        self.checkBox_isOnlySearch.setCheckState(Qt.Checked)
        self.groupBox_onlySearch.show()
        self.lineEdit_onlySearch_element.setText(data[0])
        self.lineEdit_onlySearch_toUrl.setText(data[1])
        self.lineEdit_onlySearch_image.setText(data[2])
        self.lineEdit_onlySearch_bookname.setText(data[3])
        self.lineEdit_onlySearch_author.setText(data[4])
        self.lineEdit_onlySearch_endstate.setText(data[5])
        self.lineEdit_onlySearch_latestChapter.setText(data[6])
        self.lineEdit_onlySearch_updatetime.setText(data[7])
        self.lineEdit_onlySearch_introduction.setText(data[8])

    def call_setUserRuleData_no_only_search(self, s):
        self.checkBox_isOnlySearch.setCheckState(Qt.Unchecked)
        self.groupBox_onlySearch.hide()

    def call_clearControlsText(self, s):
        for i in self.stackedWidget_rule_catalog.findChildren(QLineEdit):
            i.clear()
        for j in self.stackedWidget_rule_catalog.findChildren(QRadioButton):
            j.setChecked(False)

    def call_setCursorPositon(self, s):
        for i in self.getUserRuleLineEditControlsObject():
            if isinstance(i, QLineEdit):
                i.setCursorPosition(0)

    def call_showBookInfo(self, bookNums: int, label_process: QLabel):  # ???????????????
        self.bookIntroduction = QWidget_BookIntroduction(bookNums=bookNums, label_process=label_process)
        self.bookIntroduction.breakSignal_showReader.connect(self.call_showReader_btn)
        self.bookIntroduction.show()
        self.bookIntroduction.setFocus()

    def call_showReader_btn(self, serialNumber: int, label: QLabel):  # ????????????????????????????????????
        self.bookReader = ReadWindow(serialNumber)
        self.bookReader.breakSignal_updateBookShelfInfo.connect(self.call_updateBookShelfInfo)
        self.currentBookShelfBookLabel: QLabel = label
        self.currentBookShelfBookSerialNumber = serialNumber
        self.bookReader.show()

    def call_showReader(self, serialNumber: int):  # ???????????????
        log.info(f"??????????????????????????????serialnumber:{str(serialNumber)}")
        self.bookReader = ReadWindow(serialNumber)
        self.bookReader.breakSignal_updateBookShelfInfo.connect(self.call_updateBookShelfInfo)
        self.currentBookShelfBookLabel: QLabel = self.sender().parent().parent().findChildren(QLabel)[1]
        self.currentBookShelfBookSerialNumber = serialNumber
        self.bookReader.show()

    def call_showBookChapterList(self, num: int, frame_image: QFrame):  # ??????????????????
        self.bookChapterList = QWidget_chapterList(num=num, frame_image=frame_image)
        self.bookChapterList.setWindowModality(Qt.ApplicationModal)
        self.bookChapterList.breakSignal_sendNeedRepairChapter.connect(self.call_repair_chapter)
        self.bookChapterList.show()

    def call_updateBookShelfInfo(self, s):  # ???????????????????????????????????????
        log.info("????????????")
        try:
            user = User.UserSql()
            progress = user.selectBookShelfProgress(self.currentBookShelfBookSerialNumber)[0]
            self.currentBookShelfBookLabel.setText(f"??????:{progress}%")
        except Exception as e:
            log.error(f"??????????????????:{e}")

    def call_update_chapter(self, bookNums: int, frame_image: QFrame):  # ????????????????????????
        self.thread_update_latest_chapter = QThread_UpdateLatestChapter(bookNums=bookNums, frame_image=frame_image)
        self.thread_update_latest_chapter.breakSignal_showUpdating.connect(self.call_showUpdating)
        self.thread_update_latest_chapter.breakSignal_delUpdating.connect(self.call_delUpdating)
        self.thread_update_latest_chapter.breakSignal_setUpdatingResult.connect(self.call_setUpdatingResult)
        self.thread_update_latest_chapter.start()

    def call_updateBookShelfLayout(self, s):  # ???????????????????????????
        log.info(s)
        frame_bookshelf_line_list = self.frame_bookshelf_top.findChildren(QFrame, "frame_bookshelf_line")
        len_frame_bookshelf_line_list = len(frame_bookshelf_line_list)
        log.info(f"?????????????????????frame_line???{len_frame_bookshelf_line_list}???")
        for i in range(len_frame_bookshelf_line_list):
            hlayout_bookshelf_line: QHBoxLayout = frame_bookshelf_line_list[i].findChild(QHBoxLayout,
                                                                                         "hlayout_bookshelf_line")
            frame_book = frame_bookshelf_line_list[i].findChildren(QFrame, "frame_book")
            if len(frame_book) == 3 and i != len_frame_bookshelf_line_list - 1:
                next_frame_book_list = frame_bookshelf_line_list[i + 1].findChildren(QFrame, "frame_book")
                hlayout_bookshelf_line.insertWidget(4, next_frame_book_list[0])
                if len(next_frame_book_list) == 1:
                    next_hlayout_bookshelf_line: QHBoxLayout = frame_bookshelf_line_list[i + 1].findChild(QHBoxLayout,
                                                                                                          "hlayout_bookshelf_line")
                    next_hlayout_bookshelf_line.parent().deleteLater()

    def call_repair_chapter(self, needRepairDict: dict,
                            bookUrl: str,
                            bookRule: int,
                            frame_image: QFrame,
                            delay_time: int,
                            serialNumber: int,
                            autoRepair: int):  # ????????????
        log.info(f"?????????????????????????????????frame_book???{str(frame_image)}")
        self.thread_repair_book_chapter = QThread_RepairBookChapter(
            needRepairDict=needRepairDict,
            bookUrl=bookUrl,
            bookRule=bookRule,
            frame_image=frame_image,
            delay_time=delay_time,
            serialNumber=serialNumber,
            autoRepair=autoRepair)
        self.thread_repair_book_chapter.breakSignal_showRepairing.connect(self.call_showRepairing)
        self.thread_repair_book_chapter.breakSignal_delRepairing.connect(self.call_delUpdating)
        self.thread_repair_book_chapter.breakSignal_sendRepairResult.connect(self.call_showRepairResult)
        self.thread_repair_book_chapter.start()

    @staticmethod
    def call_delUpdating(frame_image: QFrame):  # ??????????????????????????????gif
        overlay: QFrame = frame_image.property("frame_image_mask")
        if overlay is None:
            log.info("frame_image_mask??????????????????????????????")
            return
        overlay.deleteLater()
        frame_image.setProperty("frame_image_mask", None)

    @staticmethod
    def call_showRepairResult(msg: str):
        QMessageBox_showMsg(text=msg, title="????????????", icon="").makeSure()

    @staticmethod
    def call_setUpdatingResult(image_path: str, frame_image: QFrame):
        pixmap = QPixmap(QFileInfo(f"{image_path}").absoluteFilePath())
        overlay: QFrame = frame_image.property("frame_image_mask")
        overlay_label = overlay.label_overlay
        overlay_label.setPixmap(pixmap)

    @staticmethod
    def call_showUpdating(frame_image: QFrame):  # ????????????????????????gif
        overlay = QWidget_Mask_Update_chapter(parent=frame_image)
        overlay.show()
        frame_image.setProperty("frame_image_mask", overlay)

    @staticmethod
    def call_showRepairing(frame_image: QFrame):  # ????????????????????????gif
        overlay = QWidget_Mask_Update_chapter(gif=["./Resource/repairing.gif"], parent=frame_image)
        overlay.show()
        frame_image.setProperty("frame_image_mask", overlay)

    def call_resetUserInfo(self, getStr: str, getInt: int, getInt2: int, getStr2: str, getInt3: int) -> None:  # ????????????
        self.lineEdit_setting_downloadLocation.setText(getStr)
        self.comboBox_processNums.setCurrentIndex(getInt)
        self.comboBox_parallelTasks.setCurrentIndex(getInt2)
        self.lineEdit_setting_finishMusic.setText(getStr2)
        self.comboBox_delayTime.setCurrentIndex(getInt3)
        log.info(f"??????_?????????????????????{getStr}, {str(getInt)}, {str(getInt2)}, {getStr2}")

    def call_lessBookShelfNums(self):  # ????????????????????????
        self.bookShelfLayoutNums -= 1
        log.info(f"???????????????????????????:{str(self.bookShelfLayoutNums + 1)}")
        if self.bookShelfLayoutNums + 1 == 0:
            self.frame_noneBookShelf.show()
        else:
            self.frame_noneBookShelf.hide()

    def call_setCacheImagesLabel(self, text_useless: str, text_useful: str):
        self.label_setting_cache_nomust.setText(text_useless)
        self.label_setting_cache_must.setText(text_useful)

    def call_setDebugMarkdownResult(self, markdown_html: str):  # ????????????????????????
        self.textEdit_markdown_result.insertHtml(markdown_html)

    def call_setDebugingRefreshIconStatus(self, status: bool):
        if status:
            self.label_debugrule_search_refresh_movie.start()
            self.label_debugrule_search_refresh.show()
        else:
            self.label_debugrule_search_refresh_movie.stop()
            self.label_debugrule_search_refresh.hide()

    def call_setHTML(self, s):
        self.responseHTMl = s

    def on_setLocalSQLSelectAll_clicked(self):
        checkbox_state = 0
        if self.checkBox_manage_all_choose.isChecked():
            checkbox_state = 2
        row = self.tableWidget_manage.rowCount()
        for i in range(row):
            table_widget_item: QTableWidgetItem = self.tableWidget_manage.item(i, 0)
            table_widget_item.setCheckState(checkbox_state)

    def on_delLocalSQLManage_clicked(self):  # ?????????????????????????????????
        log.info("??????????????????")
        row = self.tableWidget_manage.rowCount()
        select_list = []
        select_serial_number = []
        for i in range(row):
            table_widget_item: QTableWidgetItem = self.tableWidget_manage.item(i, 0)
            table_widget_item_checkstate = table_widget_item.checkState()
            if table_widget_item_checkstate == Qt.Checked:
                select_list.append(i)
                select_serial_number.append(self.tableWidget_manage.verticalHeaderItem(i).text())
        select_nums = len(select_list)
        if select_nums:
            makesure = QMessageBox_showMsg(text=f"????????????{select_nums}????????????", Windows=self).makeSures()
            if makesure:
                select_list.reverse()
                log.info(f"?????????:{str(select_list)}")
                log.info(f"??????serial:{str(select_serial_number)}")

                for manage_row in select_list:
                    self.tableWidget_manage.removeRow(manage_row)
                self.checkBox_manage_all_choose.setCheckState(Qt.Unchecked)
                self.thread_DeleteUserLocalSQL = QThread_DeleteUserLocalSQL(select_serial_number=select_serial_number)
                self.thread_DeleteUserLocalSQL.start()
                # self.thread_DeleteUserLocalSQL.finished.connect(lambda: self.thread_DeleteUserLocalSQL.deleteLater())
        else:
            QMessageBox_showMsg(text="??????????????????????????????", Windows=self).makeSure()

    def call_setTextEdit_model4_ajaxdata(self, text_model4_ajax_data: str):
        self.textEdit_model_4_ajaxData.setText(text_model4_ajax_data)

    def call_setTextEdit_data(self, text_data: str):
        self.textEdit_data.setText(text_data)

    def call_setPurifyLayoutData(self, sourcename: str, rexp: str, checkstate: int, replaetotext: str) -> None:
        log.info("???????????????????????? %s, %s, %d, %s" % (sourcename, rexp, checkstate, replaetotext))
        self.lineEdit_purify_replace_name.clear()
        self.textEdit_purify_replace_text.clear()
        self.checkBox_purify_userRexp.setChecked(False)
        self.textEdit_purify_replaceTo.clear()

        self.lineEdit_purify_replace_name.setText(sourcename)
        self.lineEdit_purify_replace_name.setCursorPosition(0)
        self.textEdit_purify_replace_text.setPlainText(rexp)
        self.checkBox_purify_userRexp.setCheckState(checkstate)
        self.textEdit_purify_replaceTo.setPlainText(replaetotext)

    def call_toDebugInterface(self, whichRule: int):
        self.textEdit_markdown_result.clear()
        self.stackedWidget.setCurrentIndex(6)
        self.stacked_debugRule.setProperty("whichRule", whichRule)
        log.info(f"??????????????????????????????{str(whichRule)}")

    def deleteSearchReslutItems(self) -> None:  # ???????????????????????????????????????
        log.info("???????????????????????????????????????")
        frame = self.findChildren(QFrame, "searchResultListFrame")
        for i in frame:
            i.deleteLater()
        self.label_searchNum.setText("")

    def deleteUserLocalJsonRule(self, needRemoveIndex: list):  # ????????????json????????????
        """
        :rtype: None
        """
        self.thread_DeleteUserJsonRule = QThread_DeleteUserJsonRule(needRemoveIndex=needRemoveIndex)
        # self.thread_DeleteUserJsonRule.finished.connect(lambda: self.thread_DeleteUserJsonRule.deleteLater())
        self.thread_DeleteUserJsonRule.start()

    def deleteUserLocalPurifyJsonRule(self, needRemoveIndex: list):  # ????????????json????????????
        """
        :rtype: None
        """
        self.thread_DeleteUserPurifyJsonRule = QThread_DeleteUserPurifyJsonRule(needRemoveIndex=needRemoveIndex)
        # self.thread_DeleteUserPurifyJsonRule.finished.connect(
        #     lambda: self.thread_DeleteUserPurifyJsonRule.deleteLater())
        self.thread_DeleteUserPurifyJsonRule.start()

    @staticmethod
    def deleteThreadDownloadTask(thread: QThread) -> None:  # ??????????????????
        thread.quit()
        thread.wait()
        thread.deleteLater()

    def extraPromptControlLayoutAnimation(self, bookname: str) -> None:  # ??????????????????
        if len(bookname) >= 11:
            bookname = bookname[0:10] + "..."
        self.label_tip.setText(bookname)
        self.label_tip.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.anim = QPropertyAnimation(self.frame_prompt, b"geometry", self)
        self.anim.setDuration(4500)
        # ????????? ?????????  ??????????????? ???????????????
        self.anim.setKeyValueAt(0,
                                QRect(self.width() - self.frame_prompt.width(),
                                      self.height() + 1,
                                      self.frame_prompt.width(),
                                      self.frame_prompt.height()))
        self.anim.setKeyValueAt(0.1,
                                QRect(self.width() - self.frame_prompt.width(),
                                      self.height() - self.frame_prompt.height(),
                                      self.frame_prompt.width(),
                                      self.frame_prompt.height()))
        self.anim.setKeyValueAt(0.85,
                                QRect(self.width() - self.frame_prompt.width(),
                                      self.height() - self.frame_prompt.height(),
                                      self.frame_prompt.width(),
                                      self.frame_prompt.height()))
        self.anim.setKeyValueAt(1,
                                QRect(self.width() - self.frame_prompt.width(),
                                      self.height() + 10,
                                      self.frame_prompt.width(),
                                      self.frame_prompt.height()))
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.start(self.anim.DeleteWhenStopped)

    def extraPromptControlLayout(self) -> None:  # ????????????
        self.frame_prompt = QFrame(self)
        self.label_tip = QLabel(self.frame_prompt)
        self.label_tip.setStyleSheet(
            """
            QLabel{
                background:#000000;
                color:#ffffff;
                font:16px Microsoft YaHei;
                border-top-left-radius:5px;
                border-bottom-left-radius:5px;}
            """)
        self.label_tip.setText("None")
        self.label_tip.setAlignment(Qt.AlignCenter)
        self.label_tip.adjustSize()
        self.label_tip.resize(180, 50)
        self.frame_prompt.resize(180, 50)
        self.frame_prompt.setGeometry(self.width() - self.frame_prompt.width(),
                                      self.height(),
                                      self.frame_prompt.width(),
                                      self.frame_prompt.height())

    def extraTiplayout(self) -> None:  # ????????????2
        self.frame_tips = QFrame(self.stackedWidget)
        label_tip = QLabel(self.frame_tips)
        label_tip.setStyleSheet(
            "QLabel{background:#008CBA;color:#ffffff;font:16px Microsoft YaHei;border-radius:5px;}")
        label_tip.setText("????????????")
        label_tip.setAlignment(Qt.AlignCenter)
        label_tip.adjustSize()
        label_tip.resize(120, 50)
        self.frame_tips.resize(120, 50)
        # self.frame_tips.setAttribute(Qt.WA_TranslucentBackground)
        self.GraphicsOpacityEffect = QGraphicsOpacityEffect()

        self.frame_tips.setGraphicsEffect(self.GraphicsOpacityEffect)
        self.frame_tips.hide()
        self.frame_tips.setGeometry(415,
                                    560,
                                    self.frame_tips.width(),
                                    self.frame_tips.height())

    def extraTiplayoutShow(self):  # ????????????2????????????
        self.frame_tips.show()
        self.save_tip = QPropertyAnimation(self.GraphicsOpacityEffect, b"opacity", parent=self.stackedWidget)
        self.save_tip.setDuration(1500)
        self.save_tip.setEasingCurve(QEasingCurve.InCirc)
        self.save_tip.setStartValue(1.0)
        self.save_tip.setEndValue(0.0)
        self.save_tip.start()

    def extraSetting(self) -> None:
        # global parallelDownloadNums, nowDownloadNums

        global_set_value(key="number_of_download_tasks_now", value=0)
        # nowDownloadNums = 0
        self.setWindowFlag(Qt.FramelessWindowHint)  # ??????
        self.setWindowTitle("WhiteRead")
        self.setWindowIcon(QIcon(QFileInfo("./Resource/favicon.ico").absoluteFilePath()))
        self.setAttribute(Qt.WA_TranslucentBackground)  # ????????????

        self.hlayout_Novel.setSpacing(0)
        self.vlayout_main_left.setSpacing(0)
        self.vlayout_main_left_small.setSpacing(0)
        self.widget_main_left_small.hide()  # ????????? ???????????????
        self.adjustSize()  # ????????? ??????????????????
        self.lineEdit_search.setPlaceholderText("??????/??????")  # ?????????????????????

        UserData = self.getUserSqlLite()

        # ??????????????????????????????????????????????????????
        self.lineEdit_setting_downloadLocation.setText(UserData["saveFilePath"])
        self.comboBox_processNums.setCurrentIndex(UserData["progressNum"])
        self.comboBox_parallelTasks.setCurrentIndex(UserData["parallelTasks"])
        self.lineEdit_setting_finishMusic.setText(UserData["downloadFinishMusicPath"])
        self.comboBox_delayTime.setCurrentIndex(UserData["downloadTaskDelayTime"])
        self.spinBox_setting_search_processNums.setValue(UserData["searchProcessNum"])
        # parallelDownloadNums = UserData["parallelTasks"] + 1  # ??????????????????combobox????????? ??????+1
        global_set_value("number_of_parallel_download_tasks", UserData["parallelTasks"] + 1)
        if UserData["left_widget"] == 0:
            self.btn_more.click()
        else:
            self.btn_lessmore.click()
        self.comboBox_parallelTasks.currentIndexChanged.connect(lambda: self.setRetrieveDataTamperingStatus(1))
        self.comboBox_processNums.currentIndexChanged.connect(lambda: self.setRetrieveDataTamperingStatus(1))
        self.comboBox_delayTime.currentIndexChanged.connect(lambda: self.setRetrieveDataTamperingStatus(1))
        self.lineEdit_setting_downloadLocation.setCursorPosition(0)
        self.lineEdit_setting_finishMusic.setCursorPosition(0)
        self.comboBox_searchResult_sort.setCurrentIndex(self.getUserInitComboboxIndexSearchSort())
        # ??????????????????????????????
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.vlayout_download_scrollAreaWidgetControls.addItem(spacerItem)

        self.vlayout_download_t = QVBoxLayout()
        self.frame.setLayout(self.vlayout_download_t)

        self.radioButton_post.setChecked(True)  # ????????????Post
        self.listWidget_rule_userRule.setStyleSheet("""
        background-color: rgba(255, 255, 224, 50%);
        """)
        # ????????????
        # ?????????????????????label
        self.label_setting_playSound = QLabel_playSound(self.lineEdit_setting_finishMusic)
        self.hlayout_setting_finnishMusic.insertWidget(2, self.label_setting_playSound)

        self.lineEdit_debugrule_search.setPlaceholderText("??????: ??????/??????")
        self.initAddLineEditDebugSearchBtn()
        self.label_debugrule_search_refresh_movie = QMovie(":/icon/icon/refresh2.gif")  # ?????????????????????
        self.label_debugrule_search_refresh.setMovie(self.label_debugrule_search_refresh_movie)

        # ????????????
        UserRuleHighLight(parent=self.textEdit_data, keywords=["f'\{searchName_\}'"])
        UserRuleHighLight(parent=self.textEdit_model_4_ajaxData, keywords=["\{bookid\}"])
        self.textEdit_data.setMinimumHeight(40)
        self.textEdit_model_4_ajaxData.setMinimumHeight(40)

        # ????????????
        self.tableWidget_manage.setColumnWidth(0, 50)
        self.tableWidget_manage.setColumnWidth(5, 80)
        self.tableWidget_manage.horizontalHeader().setVisible(True)
        self.tableWidget_manage.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.tableWidget_manage.setFocusPolicy(Qt.NoFocus)

    def extraCursorSetting(self) -> None:  # ?????????????????????????????????
        self.setCursor(QCursor(QPixmap(":/cursor/Cur/normal.cur"), 0, 0))
        btn = self.findChildren(QPushButton)
        linedit = self.findChildren(QLineEdit)
        # normal ?????????
        # texto ???????????????
        # work ???????????????
        # No_Disponible ?????????
        # ayuda ?????????
        for i in btn:
            i.setCursor(QCursor(QPixmap(":/cursor/Cur/work.cur"), 0, 0))
        for j in linedit:
            j.setCursor(QCursor(QPixmap(":/cursor/Cur/texto.cur"), 0, 0))

    def getFindTextAllNums(self) -> int:  # ??????????????????????????????
        findtext = self.lineEdit_getUserFindText.text()
        if self.stackedWidget_getResult.currentIndex() == 0:
            findParent = self.textEdit_getUrl_getResult_response
        else:
            findParent = self.textEdit_getUrl_getResult_preview
        num = 0
        findParent.moveCursor(QTextCursor.Start)
        while True:
            if findParent.find(findtext):
                num += 1
            else:
                break
        findParent.moveCursor(QTextCursor.Start)
        return num

    def getUserRuleLineEditControlsObject(self) -> list:  # ????????????????????????????????????
        lineEdit_obj = [
            self.lineEdit_sourceName,
            self.lineEdit_searchUrl,
            self.lineEdit_charset,
            self.lineEdit_searchList,
            self.lineEdit_image,
            self.lineEdit_bookName,
            self.lineEdit_author,
            self.lineEdit_endstate,
            self.lineEdit_latestChapter,
            self.lineEdit_updateTime,
            self.lineEdit_introduction,
            self.lineEdit_sourceUrl,
            self.lineEdit_model_1_element,
            self.lineEdit_model_1_bookUrl,
            self.lineEdit_model_1_bookName,
            self.lineEdit_model_2_element,
            self.lineEdit_model_2_toUrl,
            self.lineEdit_model_2_bookUrl,
            self.lineEdit_model_2_bookName,
            self.lineEdit_model_4_element,
            self.lineEdit_model_4_toUrl,
            self.lineEdit_model_4_bookUrl,
            self.lineEdit_model_4_bookName,
            self.lineEdit_model_4_ajaxUrl,
            self.lineEdit_text,
            self.lineEdit_toUrl,
            self.lineEdit_noneSearch,
            self.lineEdit_onlySearch_element,
            self.lineEdit_onlySearch_toUrl,
            self.lineEdit_onlySearch_image,
            self.lineEdit_onlySearch_bookname,
            self.lineEdit_onlySearch_author,
            self.lineEdit_onlySearch_endstate,
            self.lineEdit_onlySearch_latestChapter,
            self.lineEdit_onlySearch_updatetime,
            self.lineEdit_onlySearch_introduction,
            self.lineEdit_model_5_nextPageUrl,
            self.lineEdit_model_5_chapterElement,
            self.lineEdit_model_5_chapterUrl,
            self.lineEdit_model_5_chapterName,

            self.textEdit_data,
            self.textEdit_model_4_ajaxData,

            self.radioButton_model_4_ajaxMethod_get,
            self.radioButton_model_4_ajaxMethod_post,
            self.radioButton_post,
            self.radioButton_get,
            self.radioButton_model_1,
            self.radioButton_model_2,
            self.radioButton_model_3,
            self.radioButton_model_4,
            self.radioButton_model_5
        ]
        return lineEdit_obj

    @staticmethod
    def getUserSqlLite() -> dict:
        user = User.UserSql()
        user.checkDefaultTable()  # ????????????????????????
        userSelect = user.selectUserInfo()  # ??????????????????
        return userSelect

    @staticmethod
    def getUserInitComboboxIndexSearchSort() -> int:
        user = User.UserSql()
        index = user.selectComboboxSortChooseIndex()
        return index

    @staticmethod
    def getUserSqlLiteBookShelf() -> list:  # ???????????????????????????
        user = User.UserSql()
        userSelect = user.selectBookShelfLayout()
        # log.info("???????????????????????????%s"%(str(userSelect)))
        return userSelect

    @staticmethod
    def getUserSqlLiteDownload() -> list:  # ?????????????????????????????????
        user = User.UserSql()
        userSelect = user.selecDownloadLayout()
        log.info("?????????????????????????????????%s" % (str(userSelect)))
        # print("?????????????????????????????????%s"%(str(userSelect)))
        return userSelect

    @staticmethod
    def getUserSqlLiteBookShelfMaxBookNum() -> int:  # ??????????????????????????????num
        user = User.UserSql()
        userSelect = user.selectBookShelfMaxBookNum()
        log.info(f"??????????????? ????????????????????????????????????: {str(userSelect)}")
        max_book_num = userSelect[0] + 1 if userSelect[0] is not None else 0
        return max_book_num

    def getJsonRuleDictObjectText(self) -> dict:  # ??????????????????????????????????????????????????????
        method = 1 if self.radioButton_get.isChecked() else 2
        catalog_next_page = ""
        catalog_element = ""
        catalog_to_url = ""
        catalog_chapter_url = ""
        catalog_chapter_name = ""
        catalog_ajax_url = ""
        catalog_ajax_data = ""
        catalog_ajax_method = ""
        if self.radioButton_model_1.isChecked():
            catalog_model = 1
            catalog_element = self.lineEdit_model_1_element.text()
            catalog_chapter_url = self.lineEdit_model_1_bookUrl.text()
            catalog_chapter_name = self.lineEdit_model_1_bookName.text()

        elif self.radioButton_model_2.isChecked():
            catalog_model = 2
            catalog_element = self.lineEdit_model_2_element.text()
            catalog_to_url = self.lineEdit_model_2_toUrl.text()  # ?????????????????????????????????url
            catalog_chapter_url = self.lineEdit_model_2_bookUrl.text()  # ?????????url
            catalog_chapter_name = self.lineEdit_model_2_bookName.text()
        elif self.radioButton_model_3.isChecked():
            catalog_model = 3
        elif self.radioButton_model_4.isChecked():
            catalog_model = 4
            catalog_element = self.lineEdit_model_4_element.text()
            catalog_to_url = self.lineEdit_model_4_toUrl.text()
            catalog_chapter_url = self.lineEdit_model_4_bookUrl.text()
            catalog_chapter_name = self.lineEdit_model_4_bookName.text()
            catalog_ajax_url = self.lineEdit_model_4_ajaxUrl.text()
            catalog_ajax_data = self.textEdit_model_4_ajaxData.toPlainText()
            catalog_ajax_method = 1 if self.radioButton_model_4_ajaxMethod_get.isChecked() else 2
        else:
            catalog_model = 5
            catalog_next_page = self.lineEdit_model_5_nextPageUrl.text()
            catalog_element = self.lineEdit_model_5_chapterElement.text()
            catalog_chapter_url = self.lineEdit_model_5_chapterUrl.text()
            catalog_chapter_name = self.lineEdit_model_5_chapterName.text()
        if self.checkBox_isOnlySearch.isChecked():
            is_only_search = 1
        else:
            is_only_search = 0
        controls = {
            "bookSourceName": f"{self.lineEdit_sourceName.text()}",
            "bookSourceUrl": f"{self.lineEdit_sourceUrl.text()}",
            "searchUrl": f"{self.lineEdit_searchUrl.text()}",
            "charset": f"{self.lineEdit_charset.text()}",
            "method": method,
            "data": f"{self.textEdit_data.toPlainText()}",
            "searchBook": {
                "element": f"{self.lineEdit_searchList.text()}",
                "toUrl": f"{self.lineEdit_toUrl.text()}",
                "image": f"{self.lineEdit_image.text()}",
                "bookname": f"{self.lineEdit_bookName.text()}",
                "author": f"{self.lineEdit_author.text()}",
                "endstate": f"{self.lineEdit_endstate.text()}",
                "latestChapter": f"{self.lineEdit_latestChapter.text()}",
                "updateTime": f"{self.lineEdit_updateTime.text()}",
                "content": f"{self.lineEdit_introduction.text()}",
                "noneSearch": f"{self.lineEdit_noneSearch.text()}",
                "onlySearch": {
                    "isOnlySearch": f"{is_only_search}",
                    "element": f"{self.lineEdit_onlySearch_element.text()}",
                    "toUrl": f"{self.lineEdit_onlySearch_toUrl.text()}",
                    "image": f"{self.lineEdit_onlySearch_image.text()}",
                    "bookname": f"{self.lineEdit_onlySearch_bookname.text()}",
                    "author": f"{self.lineEdit_onlySearch_author.text()}",
                    "endstate": f"{self.lineEdit_onlySearch_endstate.text()}",
                    "latestChapter": f"{self.lineEdit_onlySearch_latestChapter.text()}",
                    "updateTime": f"{self.lineEdit_onlySearch_updatetime.text()}",
                    "content": f"{self.lineEdit_onlySearch_introduction.text()}"
                }
            },
            "catalog": {
                "model": catalog_model,
                "nextPage": f"{catalog_next_page}",
                "toUrl": f"{catalog_to_url}",
                "element": f"{catalog_element}",
                "bookUrl": f"{catalog_chapter_url}",
                "chapterName": f"{catalog_chapter_name}",
                "ajax": {
                    "url": f"{catalog_ajax_url}",
                    "method": f"{catalog_ajax_method}",
                    "data": f"{catalog_ajax_data}"
                }
            },
            "content": {
                "text": f"{self.lineEdit_text.text()}"
            }
        }
        return controls

    def getPurifyJsonRuleDictObjectText(self) -> dict:  # ????????????????????????????????????????????????????????????
        controls = {
            "purifySourceName": f"{self.lineEdit_purify_replace_name.text()}",
            "replaceRule": f"{self.textEdit_purify_replace_text.toPlainText()}",
            "isRexp": self.checkBox_purify_userRexp.checkState(),
            "replaceAfterText": f"{self.textEdit_purify_replaceTo.toPlainText()}"
        }
        return controls

    def getSearchResultInsertIndex(self, sort_choose: int,
                                   this_similarity: float,
                                   that_property_key: str) -> int or None:  # ??????????????????????????????????????????????????????
        children = self.findChildren(QFrame, "searchResultListFrame")
        if children is None: return None
        log.info(f"????????????,???????????????:{str(this_similarity)}")
        log.info(f"???????????????%s" % str([similar.property(f"{that_property_key}") for similar in children]))
        sort_reverse = True if sort_choose == 0 or sort_choose == 2 else False
        if sort_choose == 0:
            log.info("?????? ??????")
            children.sort(key=self.sort_key_bookname, reverse=sort_reverse)  # ????????????????????????(??????)
        elif sort_choose == 1:
            log.info("?????? ??????")
            children.sort(key=self.sort_key_bookname, reverse=sort_reverse)  # ????????????????????????(??????)
        elif sort_choose == 2:
            log.info("?????? ??????")
            children.sort(key=self.sort_key_author, reverse=sort_reverse)  # ???????????????????????????(??????)
        elif sort_choose == 3:
            log.info("?????? ??????")
            children.sort(key=self.sort_key_author, reverse=sort_reverse)  # ???????????????????????????(??????)
        log.info("??????????????????%s" % str([similar.property(f"{that_property_key}") for similar in children]))

        return self.iteration_similar_property(search_result_control=children,
                                               this_similarity=this_similarity,
                                               that_property_key=that_property_key,
                                               sort_reverse=sort_reverse)

    def getFindTextNums(self):
        findtext = "</a>"
        findParent = self.textEdit_getUrl_getResult_response
        num = 0
        while True:
            if findParent.find(findtext, QTextDocument.FindBackward):
                num += 1
            else:
                break
        log.info(f"{num}???")

    def hideNoDownload(self) -> None:  # ?????????????????????
        self.frame_noDownload.hide()

    def on_addSearchResultVSpacerDown_finished(self) -> None:  # ???????????????????????????????????????????????????
        frame = QFrame()
        vlayout = QVBoxLayout()
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vlayout.addItem(spacerItem)
        frame.setLayout(vlayout)
        frame.setObjectName("searchResultListFrame")
        self.vlayout_search_result_scrollAreaWidgetContents.addWidget(frame)

    def on_getFindTextPre_clicked(self) -> None:  # ?????????????????????
        findtext = self.lineEdit_getUserFindText.text()
        if self.stackedWidget_getResult.currentIndex() == 0:
            findParent = self.textEdit_getUrl_getResult_response
        else:
            findParent = self.textEdit_getUrl_getResult_preview
        if findParent.find(findtext, QTextDocument.FindBackward):
            self.findTextNumNow = self.findTextNumNow - 1 if self.findTextNumNow >= 0 else 0
            palette = findParent.palette()
            palette.setColor(QPalette.Highlight, palette.color(QPalette.Active, QPalette.Highlight))
            findParent.setPalette(palette)
            self.label_showFindTextNum.setText(f"{self.findTextNumNow}/{self.findTextNums}")

    def on_getFindTextNext_clicked(self) -> None:  # ?????????????????????
        findtext = self.lineEdit_getUserFindText.text()
        if self.stackedWidget_getResult.currentIndex() == 0:
            findParent = self.textEdit_getUrl_getResult_response
        else:
            findParent = self.textEdit_getUrl_getResult_preview
        if findParent.find(findtext):
            if self.findTextNumNow <= self.findTextNums:
                self.findTextNumNow = self.findTextNumNow + 1
            else:
                self.findTextNumNow = self.findTextNums
            palette = findParent.palette()
            palette.setColor(QPalette.Highlight, palette.color(QPalette.Active, QPalette.Highlight))
            findParent.setPalette(palette)
            self.label_showFindTextNum.setText(f"{self.findTextNumNow}/{self.findTextNums}")

    def on_setFindTextAllNums_textChanged(self) -> None:  # ??????????????????????????????
        log.info("start")
        self.findTextNums = self.getFindTextAllNums() if self.getFindTextAllNums() else "0"
        self.findTextNumNow = 0
        self.label_showFindTextNum.setText(f"0/{self.findTextNums}")
        log.info(str(self.findTextNums))

    def on_btnBookShelf_clicked(self) -> None:
        self.retrieveDataTampering()
        self.stackedWidget.setCurrentIndex(1)
        self.changeBtnFont("self.frame_main_down_bookshelf,self.frame_main_down_bookshelf_small")

    def on_btnGetBook_clicked(self) -> None:
        self.retrieveDataTampering()
        self.stackedWidget.setCurrentIndex(0)
        self.changeBtnFont("self.frame_main_down_getbook_small")
        # self.lineEdit_search.setFocus()

    def on_btnDownload_clicked(self) -> None:
        self.retrieveDataTampering()
        self.stackedWidget.setCurrentIndex(3)
        self.changeBtnFont("self.frame_main_down_download,self.frame_main_down_download_small")

    def on_btnRule_clicked(self) -> None:
        self.retrieveDataTampering()
        self.stackedWidget.setCurrentIndex(2)
        self.changeBtnFont("self.frame_main_down_rule,self.frame_main_down_rule_small")

    def on_btnXpath_clicked(self) -> None:
        self.retrieveDataTampering()
        self.stackedWidget.setCurrentIndex(4)
        self.changeBtnFont("self.frame_main_down_xpath,self.frame_main_down_xpath_small")

    def on_btnSetting_clicked(self) -> None:
        self.stackedWidget.setCurrentIndex(5)
        self.changeBtnFont("self.frame_main_down_setting,self.frame_main_down_setting_small")
        self.initCacheImagesEvent()

    def on_btnManage_clicked(self) -> None:  # ????????????
        self.retrieveDataTampering()
        self.stackedWidget.setCurrentIndex(7)
        self.changeBtnFont("self.frame_main_down_manage,self.frame_main_down_manage_small")

    def on_btnRuleDel_clicked(self) -> None:  # ????????????
        checkd_obj = []
        for index in range(self.listWidget_rule_userRule.count()):
            item = self.listWidget_rule_userRule.item(index)
            item_widget = self.listWidget_rule_userRule.itemWidget(item)
            left_check_box: QCheckBox = item_widget.findChild(QCheckBox, "rule_leftCheckBox")
            if left_check_box.checkState() == Qt.Checked:
                log.info("?????????%s" % self.listWidget_rule_userRule.item(index).text())
                checkd_obj.append(index)

        log.info(str(checkd_obj))
        if len(checkd_obj) == 0:
            QMessageBox_showMsg(text="?????????????????????????????????", Windows=self).makeSure()
        checkd_obj.reverse()
        for i in checkd_obj:
            self.listWidget_rule_userRule.takeItem(i)

        self.deleteUserLocalJsonRule(checkd_obj)
        self.update_self_rule()

    def on_btnPurifyRuleDel_clicked(self) -> None:  # ??????????????????
        checkd_obj = []
        for index in range(self.listWidget_purify.count()):
            item = self.listWidget_purify.item(index)
            item_widget = self.listWidget_purify.itemWidget(item)
            left_check_box: QCheckBox = item_widget.findChild(QCheckBox, "purify_rule_leftCheckBox")
            if left_check_box.checkState() == Qt.Checked:
                log.info("?????????%s" % self.listWidget_purify.item(index).text())
                checkd_obj.append(index)
        log.info(str(checkd_obj))
        if len(checkd_obj) == 0:
            QMessageBox_showMsg(text="?????????????????????????????????", Windows=self).makeSure()
        checkd_obj.reverse()
        for i in checkd_obj:
            self.listWidget_purify.takeItem(i)

        self.deleteUserLocalPurifyJsonRule(checkd_obj)
        self.update_self_purify_rule()

    @staticmethod
    def on_btnImportLocally_clicked() -> None:  # ????????????
        local_json = QFileDialog.getOpenFileName(None, "????????????json??????", os.getcwd(),
                                                 "json?????? (*.json)")
        if local_json[0]:
            log.info("?????????json???%s" % str(local_json[0]))

    @staticmethod
    def on_btnImportPurifyLocally_clicked() -> None:  # ????????????????????????
        local_json = QFileDialog.getOpenFileName(None, "????????????json??????", os.getcwd(),
                                                 "json?????? (*.json)")
        if local_json[0]:
            log.info("?????????json???%s" % str(local_json[0]))

    def on_btnImportNet_clicked(self) -> None:  # ????????????
        self.QDialogReadNetJson = QDialog_ReadNetJson(Windows=self)
        self.QDialogReadNetJson.setWindowFlag(Qt.FramelessWindowHint)
        self.QDialogReadNetJson.setWindowModality(Qt.ApplicationModal)
        self.QDialogReadNetJson.btn_read_net.clicked.connect(lambda: self.btnReadNetJson(self.QDialogReadNetJson))
        self.QDialogReadNetJson.btn_cancel.clicked.connect(lambda: self.QDialogReadNetJson.close())
        self.QDialogReadNetJson.show()

    def on_btnPurifyImportNet_clicked(self) -> None:  # ????????????
        self.QDialogPurifyReadNetJson = QDialog_ReadNetJson(Windows=self)
        self.QDialogPurifyReadNetJson.setWindowFlag(Qt.FramelessWindowHint)
        self.QDialogPurifyReadNetJson.setWindowModality(Qt.ApplicationModal)
        self.QDialogPurifyReadNetJson.btn_read_net.clicked.connect(
            lambda: self.btnPurifyReadNetJson(self.QDialogReadNetJson))
        self.QDialogPurifyReadNetJson.btn_cancel.clicked.connect(lambda: self.QDialogPurifyReadNetJson.close())
        self.QDialogPurifyReadNetJson.show()

    def on_btnAddListRule_clicked(self) -> None:  # ??????listwidget??????
        new_rule_name = "????????????" + str(self.listWidget_rule_userRule.count() + 1)
        self.addNewRuleLayout(bookSourceName=new_rule_name, enable=False)
        log.info("????????????rule")
        self.thread_AddNewRule = QThread_AddNewRule(newRuleName=new_rule_name)
        self.thread_AddNewRule.start()

    def on_btnAddListPurify_clicked(self) -> None:  # ????????????listwidget??????
        new_purify_name = "????????????" + str(self.listWidget_purify.count() + 1)
        self.addNewPurifyLayout(purifySourceName=new_purify_name, enable=False)
        log.info("????????????purify")
        self.thread_AddNewPurify = QThread_AddNewPurify(newPurifyName=new_purify_name)
        self.thread_AddNewPurify.finished.connect(self.update_self_purify_rule)
        self.thread_AddNewPurify.start()

    def on_clearImageCache_clicked(self):
        images_path = self.selectUsefulImageCache()
        if len(images_path) == 0:
            log.info("????????????????????????")

        self.thread_clear_cache = QThread_Clear_Cache()
        self.thread_clear_cache.breakSignal_setLabel.connect(self.call_setCacheImagesLabel)
        self.thread_clear_cache.start()

    def on_hide_show_Widget_clicked(self):
        if self.sender() == self.btn_lessmore:
            self.widget_main_left.hide()
            self.widget_main_left_small.show()
            self.adjustSize()
            self.thread_update_usersql_leftwidget = threadUpdateUserSQLLeftWidget(status=1)
            self.thread_update_usersql_leftwidget.start()
            # self.thread_update_usersql_leftwidget.finished.connect(
            #     lambda: self.thread_update_usersql_leftwidget.deleteLater())
        else:
            self.widget_main_left_small.hide()
            self.widget_main_left.show()
            self.adjustSize()
            self.thread_update_usersql_leftwidget = threadUpdateUserSQLLeftWidget(status=0)
            self.thread_update_usersql_leftwidget.start()
            # self.thread_update_usersql_leftwidget.finished.connect(
            #     lambda: self.thread_update_usersql_leftwidget.deleteLater())

    @pyqtSlot(QPoint)
    def on_listWidget_rule_userRule_customContextMenuRequested(self, point: QPoint):
        log.info("??????")
        controls = self.listWidget_rule_userRule.itemAt(point)
        row = self.listWidget_rule_userRule.row(controls)
        if row != -1:
            debug_menu = QMenu_DebugUserRule(whichRule=row)
            debug_menu.breakSignal_toDebugInterface.connect(self.call_toDebugInterface)
            debug_menu.exec_(QCursor.pos())

    def on_listWidgetRuleDoubleClickEvent_doubleClicked(self, s: QModelIndex) -> None:  # ????????????????????????
        # Qt.NonModal ????????????????????????
        # Qt.WindowModal ????????????????????????????????????????????????????????????????????????????????????????????????
        # Qt.ApplicationModal ????????????????????????????????????????????????????????????????????????????????????
        # example: self.setWindowModality(Qt.ApplicationModal)
        log.info("?????????%s???" % str(s.row()))
        self.update_self_rule()
        self.btn_rule_save.setProperty("now_row", s.row())
        try:
            self.readRuleThread = QThread_ReadRule(now_rule=self.rule[s.row()])
            self.readRuleThread.breakSignal_setUserRuleData.connect(self.call_setUserRuleData)
            self.readRuleThread.breakSignal_setUserRuleData_model_1.connect(self.call_setUserRuleDataModelOne)
            self.readRuleThread.breakSignal_setUserRuleData_model_2.connect(self.call_setUserRuleDataModelTwo)
            self.readRuleThread.breakSignal_setUserRuleData_model_3.connect(self.call_setUserRuleDataModelThree)
            self.readRuleThread.breakSignal_setUserRuleData_model_4.connect(self.call_setUserRuleDataModelFour)
            self.readRuleThread.breakSignal_setUserRuleData_model_5.connect(self.call_setUserRuleDataModelFive)
            self.readRuleThread.breakSignal_setUserRuleData_only_search.connect(self.call_setUserRuleData_only_search)
            self.readRuleThread.breakSignal_setUserRuleData_no_only_search.connect(
                self.call_setUserRuleData_no_only_search)
            self.readRuleThread.breakSignal_clearControlsText.connect(self.call_clearControlsText)
            self.readRuleThread.breakSignal_setCursorPositon.connect(self.call_setCursorPositon)
            self.readRuleThread.start()
            self.update()
        except Exception as err:
            log.error(err)

    def on_purify_listWidgetRuleDoubleClickEvent_doubleClicked(self, s: QModelIndex) -> None:
        # Qt.NonModal ????????????????????????
        # Qt.WindowModal ????????????????????????????????????????????????????????????????????????????????????????????????
        # Qt.ApplicationModal ????????????????????????????????????????????????????????????????????????????????????
        # self.setWindowModality(Qt.ApplicationModal)
        log.info("?????????%s???" % str(s.row()))
        self.btn_purify_save.setProperty("now_row", s.row())

        try:
            self.readPurifyRuleThread = QThread_ReadPurifyRule(now_purify_rule=self.purify_rule[s.row()])
            self.readPurifyRuleThread.breakSignal_setPurifyLayoutData.connect(self.call_setPurifyLayoutData)
            self.readPurifyRuleThread.start()
            self.update()
        except Exception as err:
            log.error(err)

    def on_refreshManageLayout_clicked(self):  # ????????????????????????
        row = self.tableWidget_manage.rowCount()
        for i in range(row):
            self.tableWidget_manage.removeRow(0)
            self.tableWidget_manage.update()
            self.update()
        self.initManageLocalSQLLayout()

    def on_rule_choose_item_stateChanged(self, enable: int):
        selectItem: QCheckBox = self.sender().property("QListWidgetItem")
        selectIndex = self.listWidget_rule_userRule.row(selectItem)
        self.thread_update_user_rule_enable = QThread_UpdateUserRuleEnable(selectIndex=selectIndex, enable=enable)
        self.thread_update_user_rule_enable.breakSignal_isSuccess.connect(self.call_getUpdateUserRuleEnableStatus)
        self.thread_update_user_rule_enable.start()

    def on_purify_choose_item_stateChanged(self, enable: int):
        selectItem: QCheckBox = self.sender().property("QListWidgetItem_purify")
        selectIndex = self.listWidget_purify.row(selectItem)
        self.thread_update_purify_rule_enable = QThread_UpdatePurifyRuleEnable(selectIndex=selectIndex, enable=enable)
        self.thread_update_purify_rule_enable.breakSignal_isSuccess.connect(self.call_getUpdatePurifyRuleEnableStatus)
        self.thread_update_purify_rule_enable.start()

    def on_saveUserChooseFilePath_clicked(self) -> None:
        directory = QFileDialog.getExistingDirectory(None, "?????????????????????????????????", self.lineEdit_setting_downloadLocation.text())
        if directory:
            log.info("????????????????????????????????????%s" % directory)
            self.lineEdit_setting_downloadLocation.setText(directory)
            self.retrieveDataTamperingStatus = 1

    def on_saveUSerChooseMusicPath_clicked(self) -> None:
        music = QFileDialog.getOpenFileName(None, "???????????????????????????", self.lineEdit_setting_finishMusic.text(),
                                            "?????? (*.wav)")
        if music[0]:
            log.info("??????????????????%s" % music[0])
            self.lineEdit_setting_finishMusic.setText(music[0])
            self.retrieveDataTamperingStatus = 1

    def on_setOnlySearchVisible_clicked(self, ischeck: bool):
        if ischeck:
            self.groupBox_onlySearch.show()
        else:
            self.groupBox_onlySearch.hide()

    def on_shrinkdownToPallets_clicked(self) -> None:  # ???????????????
        try:
            self.trayIcon = QSystemTrayIcon_Background(self)
            self.hide()
            self.trayIcon.show()

        except Exception as err:
            log.error(err)

    def on_startSearchThreadEvent_clicked_returnPressed(self) -> None:  # ?????????????????????
        searchText = self.lineEdit_search.text().replace(" ", "")
        if searchText != "":
            self.retrieveDataTampering()
            self.on_btnGetBook_clicked()
            self.deleteSearchReslutItems()
            self.label_refresh.hide()  # ????????????????????????????????????
            self.label_refresh.show()  # ????????????
            self.frame_noneSearch.hide()  # ?????????????????????
            self.label_searchNum.clear()  # ????????????
            self.loding_movie.start()  # ???????????????gif
            self.frame_loding.show()
            self.setSearchThreadStop()
            self.searchThread = QThread_Search(searchText, self.rule)
            self.searchThread.breakSignal_str_hideLodingGif.connect(self.call_addSearchResultHideLodingGif)  # ??????????????????gif
            self.searchThread.breakSignal_addSearchResult.connect(self.call_addSearchResult)  # ??????????????????????????????
            self.searchThread.breakSignal_NoneSearch.connect(self.call_addSearchResultShowNoneSearch)  # ????????????????????????
            self.searchThread.breakSignal_int_showSearchNums.connect(
                self.call_addSearchResultShowSearchNums)  # ??????????????????????????????
            self.searchThread.finished.connect(self.on_setSearchThreadStart_finished)
            self.searchThread.finished.connect(self.call_addSearchResultHideLodingGif)
            self.searchThread.finished.connect(self.call_addSearchResultHideReflushIcon)
            self.searchThread.finished.connect(self.on_addSearchResultVSpacerDown_finished)
            self.searchThread.start()
            log.info("???????????????%s" % searchText)
        elif self.lineEdit_search.text() == "":
            log.info("?????????")
            showMsg = QMessageBox_showMsg(icon="./Resource/tip.png", text="??????????????????/??????", Windows=self)
            showMsg.hideIcon()
            showMsg.makeSure()
        else:
            log.info("????????????")
            showMsg = QMessageBox_showMsg(icon="./Resource/tip.png", text="??????????????????", Windows=self)
            showMsg.hideIcon()
            showMsg.makeSure()

    def on_stopSearchThreadEvent_clicked(self):
        self.call_addSearchResultHideLodingGif()
        self.call_addSearchResultHideReflushIcon()
        self.on_setSearchThreadStart_finished()
        try:
            self.searchThread.terminate()
            self.searchThread.wait()  # ??????????????????
            if self.searchThread.isFinished():  # ????????????????????????????????????????????????
                del self.searchThread
        except Exception:
            pass

    def on_setSearchThreadStart_finished(self):
        self.btn_search_image.setStyleSheet("""
                QPushButton#btn_search_image{
                    border-image:url('./Resource/icon/nsearch48.png');
                }
                QPushButton#btn_search_image:hover{
                    border-image:url('./Resource/icon/npsearch48.png');
                }
                QPushButton#btn_search_image:pressed{
                    border-image:url('./Resource/icon/nsearch48.png');
                    background-color: #0078d7;
                }
            """)
        self.btn_search_image.clicked.disconnect()
        self.btn_search_image.clicked.connect(self.on_startSearchThreadEvent_clicked_returnPressed)

    def on_startDebugThreadEvent_clicked(self) -> None:
        log.info("??????????????????????????????")
        self.setDebugThreadStop()
        self.textEdit_markdown_result.clear()
        self.thread_debug = QThread_Debug(
            debug_searchName=self.lineEdit_debugrule_search.text(),
            whichRule=self.stacked_debugRule.property("whichRule"))
        self.thread_debug.breakSignal_setDebugMarkdownResult.connect(self.call_setDebugMarkdownResult)
        self.thread_debug.breakSignal_setDebugingRefreshIconStatus.connect(self.call_setDebugingRefreshIconStatus)
        self.thread_debug.finished.connect(self.on_setDebugThreadStart_finished)
        self.thread_debug.start()

    def on_stopDebugThreadEvent_clicked(self):
        self.call_setDebugingRefreshIconStatus(status=False)
        try:
            self.thread_debug.terminate()
            self.thread_debug.wait()  # ??????????????????
            if self.thread_debug.isFinished():  # ????????????????????????????????????????????????
                del self.thread_debug
        except Exception:
            pass

    def on_setDebugThreadStart_finished(self):
        self.btn_debug.setStyleSheet("""
                QPushButton#btn_debug{
                    border-image:url('./Resource/icon/nsearch48.png');
                }
                QPushButton#btn_debug:hover{
                    border-image:url('./Resource/icon/npsearch48.png');
                }
                QPushButton#btn_debug:pressed{
                    border-image:url('./Resource/icon/nsearch48.png');
                    background-color: #0078d7;
                }
            """)
        self.btn_debug.clicked.disconnect()
        self.btn_debug.clicked.connect(self.on_startDebugThreadEvent_clicked)

    def on_threadUserDataSave_clicked(self) -> None:  # ???????????????????????????
        log.info("??????->?????????????????????%s" % self.lineEdit_setting_downloadLocation.text())
        log.info("??????->?????????????????????%s" % str(self.comboBox_processNums.currentIndex()))
        log.info("??????->?????????????????????%s" % str(self.comboBox_parallelTasks.currentIndex()))
        log.info("??????->????????????????????????%s" % self.lineEdit_setting_finishMusic.text())
        log.info("??????->???????????????%s" % str(self.comboBox_delayTime.currentIndex()))
        log.info("??????->??????????????????:%s" % str(self.spinBox_setting_search_processNums.value()))
        if not os.path.exists(self.lineEdit_setting_downloadLocation.text()):
            log.info("?????????????????????")
            QMessageBox_showMsg(title="???????????????", text=f"{self.lineEdit_setting_downloadLocation.text()} ??????????????????",
                                Windows=self).makeSure()
            return
        if not os.path.isfile(self.lineEdit_setting_finishMusic.text()):
            log.info("????????????????????????")
            QMessageBox_showMsg(title="???????????????", text=f"{self.lineEdit_setting_finishMusic.text()} ?????????????????????",
                                Windows=self).makeSure()
            return
        self.retrieveDataTamperingStatus = 0
        self.threadUserDataSave_ = QThread_UserData(
            self.lineEdit_setting_downloadLocation.text(),
            self.comboBox_processNums.currentIndex(),
            self.comboBox_parallelTasks.currentIndex(),
            self.lineEdit_setting_finishMusic.text(),
            self.comboBox_delayTime.currentIndex(),
            self.spinBox_setting_search_processNums.value()
        )
        self.threadUserDataSave_.breakSignal_UserData.connect(self.call_saveUserInfo)
        self.threadUserDataSave_.start()

    def on_threadUserDataReset_clicked(self) -> None:  # ???????????????????????????
        self.threadUserDataReset_ = QThread_UserData()
        self.threadUserDataReset_.breakSignal_UserData.connect(self.call_resetUserInfo)
        self.threadUserDataReset_.start()

    def on_threadXpath_clicked(self) -> None:  # ????????????xpath?????????
        self.textEdit_getUrl_getResult_response.clear()
        self.textEdit_getUrl_getResult_preview.clear()
        self.textEdit_getUrl_getResult_response.append(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: ????????????????????????...')
        self.textEdit_getUrl_getResult_preview.insertHtml(
            f"<font color='red'>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:</font> ????????????????????????...<br />")

        self.threadXpath_ = QThread_Xpath(
            url=self.lineEdit_getUrl_url.text(),
            charset=self.lineEdit_getUrl_charset.text(),
            method=self.comboBox_getUrl_method.currentIndex(),
            headers=self.textEdit_getUrl_headers.toPlainText(),
            data=self.textEdit_getUrl_data.toPlainText()
        )
        self.threadXpath_.breakSignal_appendResultText.connect(self.call_appendResultText)
        self.threadXpath_.breakSignal_insertResultHTML.connect(self.call_insertResultHTML)
        self.threadXpath_.breakSignal_setHTML.connect(self.call_setHTML)
        self.threadXpath_.start()

    def on_threadXpathParseOne_clicked(self) -> None:  # ????????????xpath????????????????????????html 1
        self.textEdit_testXpath_getResult.clear()
        self.threadXpathParseOne_ = QThread_Xpath_parse_one(
            xpath=self.lineEdit_testXpath_getText.text(),
            responseHTMl=self.responseHTMl
        )
        self.threadXpathParseOne_.breakSignal_insertTestXpathHTML.connect(self.call_insertTestXpathHTML)
        self.threadXpathParseOne_.start()

    def on_threadXpathParseTwo_clicked(self) -> None:  # ????????????xpath????????????????????????html 2
        self.textEdit_testXpath_getResult.clear()

        self.threadXpathParseTwo_ = QThread_Xpath_parse_two(
            element=self.lineEdit_testXpath_two_element.text(),
            xpath=self.lineEdit_testXpath_two_element_child.text(),
            responseHTMl=self.responseHTMl,
        )
        self.threadXpathParseTwo_.breakSignal_insertTestXpathHTML.connect(self.call_insertTestXpathHTML)
        self.threadXpathParseTwo_.start()

    def retrieveDataTampering(self):  # ??????????????????
        if self.retrieveDataTamperingStatus:
            status = QMessageBox_showMsg(title="??????", text="??????????????????", Windows=self).makeSures()
            if status:
                self.on_threadUserDataSave_clicked()
            self.retrieveDataTamperingStatus = 0

    def search_result_sort(self, index: int):  # ????????????????????????
        log.info(f"????????????{str(index)}")
        user = User.UserSql()
        user.updateComboboxSortChooseIndex(index=index)
        all_frame = self.findChildren(QFrame, "searchResultListFrame")
        children = all_frame[:-1]
        vSpacer: QFrame = all_frame[-1] if all_frame else None
        if vSpacer is not None:
            vSpacer.deleteLater()
        if children is None:
            return None
        sort_reverse = True if index == 0 or index == 2 else False
        log.info("???????????????%s" % str([similar.property("bookname_similarity") for similar in children]))
        if index == 0 or index == 1:
            log.info(f"???????????? {str(sort_reverse)}")
            children.sort(key=self.sort_key_bookname, reverse=sort_reverse)
            log.info("??????????????????%s" % str([similar.property("bookname_similarity") for similar in children]))
        elif index == 2 or index == 3:
            log.info(f"???????????? {str(sort_reverse)}")
            children.sort(key=self.sort_key_author, reverse=sort_reverse)
            log.info("??????????????????%s" % str([similar.property("author_similarity") for similar in children]))
        for i in range(len(children)):
            self.vlayout_search_result_scrollAreaWidgetContents.addWidget(children[i])
        self.on_addSearchResultVSpacerDown_finished()

    def setEvent(self) -> None:
        self.btn_main.clicked.connect(self.on_btnBookShelf_clicked)  # ????????????1 ???????????????
        self.btn_download.clicked.connect(self.on_btnDownload_clicked)  # ????????????3 ???????????????
        self.btn_setting.clicked.connect(self.on_btnSetting_clicked)  # ????????????5 ???????????????
        self.btn_rule.clicked.connect(self.on_btnRule_clicked)  # ????????????2 ???????????????
        self.btn_xpath.clicked.connect(self.on_btnXpath_clicked)  # ????????????4 ???xpath??????
        self.btn_manage.clicked.connect(self.on_btnManage_clicked)  # ????????????7 ???????????????

        self.btn_main_small.clicked.connect(self.on_btnBookShelf_clicked)  # ????????????1 ???????????????
        self.btn_getbook_small.clicked.connect(self.on_btnGetBook_clicked)  # ????????????0 ???????????????
        self.btn_download_small.clicked.connect(self.on_btnDownload_clicked)  # ????????????3 ???????????????
        self.btn_setting_small.clicked.connect(self.on_btnSetting_clicked)  # ????????????5 ???????????????
        self.btn_rule_small.clicked.connect(self.on_btnRule_clicked)  # ????????????2 ???????????????
        self.btn_xpath_small.clicked.connect(self.on_btnXpath_clicked)  # ????????????4 ???xpath??????
        self.btn_manage_small.clicked.connect(self.on_btnManage_clicked)  # ????????????7 ???????????????

        self.btn_green.clicked.connect(lambda: self.showMinimized())  # ?????????
        self.btn_yellow.clicked.connect(self.on_shrinkdownToPallets_clicked)  # ???????????????
        self.btn_red.clicked.connect(lambda: self.close())  # ??????

        self.btn_green.setToolTip("?????????")
        self.btn_yellow.setToolTip("???????????????")
        self.btn_red.setToolTip("??????")

        self.btn_lessmore.clicked.connect(self.on_hide_show_Widget_clicked)  # ????????????
        self.btn_more.clicked.connect(self.on_hide_show_Widget_clicked)

        # main????????????
        self.lineEdit_search.returnPressed.connect(
            self.on_startSearchThreadEvent_clicked_returnPressed)  # ??????????????????????????????????????????
        self.comboBox_searchResult_sort.currentIndexChanged.connect(self.search_result_sort)  # ????????????????????????

        # ??????????????????
        self.listWidget_rule_userRule.doubleClicked.connect(
            self.on_listWidgetRuleDoubleClickEvent_doubleClicked)  # ?????????????????????????????????
        self.listWidget_rule_userRule.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWidget_purify.doubleClicked.connect(
            self.on_purify_listWidgetRuleDoubleClickEvent_doubleClicked)  # ???????????????????????????????????????
        self.btn_rule_del.clicked.connect(self.on_btnRuleDel_clicked)  # ??????????????????
        self.btn_purify_del_listwidget.clicked.connect(self.on_btnPurifyRuleDel_clicked)  # ????????????????????????
        self.btn_rule_local_import.clicked.connect(self.on_btnImportLocally_clicked)  # ????????????????????????
        self.btn_purify_local_import.clicked.connect(self.on_btnImportPurifyLocally_clicked)  # ????????????????????????
        self.btn_rule_net_import.clicked.connect(self.on_btnImportNet_clicked)  # ????????????????????????
        self.btn_purify_net_import.clicked.connect(self.on_btnPurifyImportNet_clicked)  # ??????????????????????????????
        self.btn_rule_add.clicked.connect(self.on_btnAddListRule_clicked)  # ??????listwidget??????
        self.btn_purify_add_listwidget.clicked.connect(self.on_btnAddListPurify_clicked)  # ??????????????????listwidget??????
        self.btn_rule_save.clicked.connect(self.btnSaveRule)  # ??????????????????
        self.btn_purify_save.clicked.connect(self.btnPurifySaveRule)  # ????????????????????????

        self.radioButton_model_1.clicked.connect(lambda: self.stackedWidget_rule_catalog.setCurrentIndex(0))
        self.radioButton_model_2.clicked.connect(lambda: self.stackedWidget_rule_catalog.setCurrentIndex(1))
        self.radioButton_model_3.clicked.connect(lambda: self.stackedWidget_rule_catalog.setCurrentIndex(2))
        self.radioButton_model_4.clicked.connect(lambda: self.stackedWidget_rule_catalog.setCurrentIndex(3))
        self.radioButton_model_5.clicked.connect(lambda: self.stackedWidget_rule_catalog.setCurrentIndex(4))
        self.checkBox_isOnlySearch.clicked.connect(self.on_setOnlySearchVisible_clicked)
        self.btn_backtorule.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        # ?????? ????????????
        self.lineEdit_setting_downloadLocation.textChanged.connect(lambda: self.setRetrieveDataTamperingStatus(1))
        self.lineEdit_setting_finishMusic.textChanged.connect(lambda: self.setRetrieveDataTamperingStatus(1))
        self.spinBox_setting_search_processNums.valueChanged.connect(lambda: self.setRetrieveDataTamperingStatus(1))
        self.btn_setting_cache_clear.clicked.connect(self.on_clearImageCache_clicked)

        self.btn_setting_downloadLocation.clicked.connect(self.on_saveUserChooseFilePath_clicked)
        self.btn_setting_finishMusic.clicked.connect(self.on_saveUSerChooseMusicPath_clicked)

        self.btn_setting_save.clicked.connect(self.on_threadUserDataSave_clicked)  # ???????????????????????????
        self.btn_setting_reset.clicked.connect(self.on_threadUserDataReset_clicked)  # ?????????????????????

        # ????????????
        self.checkBox_manage_all_choose.clicked.connect(self.on_setLocalSQLSelectAll_clicked)
        self.btn_manage_refresh.clicked.connect(self.on_refreshManageLayout_clicked)
        self.btn_manage_del.clicked.connect(self.on_delLocalSQLManage_clicked)

    @staticmethod
    def selectUsefulImageCache() -> list:
        user = User.UserSql()
        images_path = user.selectCacheImages()
        return images_path

    def setSearchThreadStop(self):
        self.btn_search_image.setStyleSheet("""
                QPushButton#btn_search_image{
                    border-image:url('./Resource/icon/searchStop48.png');
                }
                QPushButton#btn_search_image:hover{
                    border-image:url('./Resource/icon/nsearchStop48.png');
                }
                QPushButton#btn_search_image:pressed{
                    border-image:url('./Resource/icon/searchStop48.png');
                    background-color: #0078d7;
                }
            """)
        self.btn_search_image.clicked.disconnect()
        self.btn_search_image.clicked.connect(self.on_stopSearchThreadEvent_clicked)

    def setDebugThreadStop(self):
        self.btn_debug.setStyleSheet("""
                QPushButton#btn_debug{
                    border-image:url('./Resource/icon/searchStop48.png');
                }
                QPushButton#btn_debug:hover{
                    border-image:url('./Resource/icon/nsearchStop48.png');
                }
                QPushButton#btn_debug:pressed{
                    border-image:url('./Resource/icon/searchStop48.png');
                    background-color: #0078d7;
                }
            """)
        self.btn_debug.clicked.disconnect()
        self.btn_debug.clicked.connect(self.on_stopDebugThreadEvent_clicked)

    def setRetrieveDataTamperingStatus(self, status: int) -> None:
        self.retrieveDataTamperingStatus = status

    @staticmethod
    def sort_key_bookname(key: QFrame):
        return key.property("bookname_similarity")

    @staticmethod
    def sort_key_author(key: QFrame):
        return key.property("author_similarity")

    def testCursor(self):
        findtext = "</a>"
        findParent = self.textEdit_getUrl_getResult_response
        if findParent.find(findtext):
            log.info("??????")
            palette = findParent.palette()
            log.info(str(palette))
            palette.setColor(QPalette.Highlight, palette.color(QPalette.Active, QPalette.Highlight))
            findParent.setPalette(palette)

    def initAddNoBookShelf(self) -> None:  # ???????????????????????????
        self.frame_noneBookShelf = QFrame(self.scrollArea_bookshelf)
        frame_toSearch = QFrame()
        vlayout_noneBookShelf = QVBoxLayout()
        hlayout_toSearch = QHBoxLayout()
        btn_image_noneBookShelf = QPushButton()
        label_tip_noneBookShelf = QLabel("????????????????????????????????????")
        btn_toSearch = QPushButton("?????????")

        btn_image_noneBookShelf.setStyleSheet('border-image:url("./Resource/noneBookShelf.png");')
        btn_image_noneBookShelf.setMinimumSize(300, 300)
        btn_image_noneBookShelf.setMaximumSize(300, 300)
        btn_image_noneBookShelf.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        label_tip_noneBookShelf.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        btn_toSearch.clicked.connect(self.on_btnGetBook_clicked)
        btn_toSearch.setStyleSheet("background-color:red")
        btn_toSearch.setObjectName("btn_toSearch")
        btn_toSearch.setMinimumSize(100, 35)
        btn_toSearch.setMaximumSize(100, 35)
        btn_toSearch.setStyleSheet("""
                        QPushButton#btn_toSearch{border-radius: 6px;
                            line-height: 1.5;
                            background: #ca0609;
                            color: #fff;
                            font-weight: 700;
                            text-align: center;
                            padding: 6px;
                            border: 2px solid #E5E5E5;
                        }
                        QPushButton#btn_toSearch:pressed{
                            background: #ab0507;
                        }
                        """)
        vlayout_noneBookShelf.addWidget(btn_image_noneBookShelf)
        vlayout_noneBookShelf.addWidget(label_tip_noneBookShelf)
        # vlayout_noneBookShelf.addWidget(btn_toSearch)
        hlayout_toSearch.addWidget(btn_toSearch)
        frame_toSearch.setLayout(hlayout_toSearch)

        vlayout_noneBookShelf.addWidget(frame_toSearch)
        vlayout_noneBookShelf.setAlignment(Qt.AlignCenter)

        toLeft = self.stacked_bookshelf.width() - btn_image_noneBookShelf.width() - 85
        toTop = self.stacked_bookshelf.height() - btn_image_noneBookShelf.height() - 80
        self.frame_noneBookShelf.setGeometry(toLeft, toTop, btn_image_noneBookShelf.width() + 100,
                                             btn_image_noneBookShelf.height() + 100)
        self.frame_noneBookShelf.setLayout(vlayout_noneBookShelf)
        self.frame_noneBookShelf.setObjectName("frame_noneBookShelf")
        self.frame_noneBookShelf.hide()

    def initAddBookShelf(self) -> None:  # ????????????????????????
        bookshelflayoutinfo = self.getUserSqlLiteBookShelf()
        self.bookShelfLayoutNums += len(bookshelflayoutinfo)
        log.info(f"??????:{str(self.bookShelfLayoutNums)}????????????????????????")
        if bookshelflayoutinfo:
            is_row = 0
            for lineInfo in bookshelflayoutinfo:
                is_row += 1
                if is_row % 4 == 1:  # ??????1 ???????????????????????? 1%4 =1 5%4==1
                    frame_bookshelf_line = QFrame()  # ???frame
                    frame_bookshelf_line.setObjectName("frame_bookshelf_line")
                    hlayout_bookshelf_line = QHBoxLayout()  # ?????????
                    hlayout_bookshelf_line.setObjectName("hlayout_bookshelf_line")
                    log.info("?????????hlayout%s" % str(hlayout_bookshelf_line))
                # bookRow = lineInfo[0]
                book_image_path: str = lineInfo[0]
                log.info(f"??????????????????{book_image_path}")
                book_name = lineInfo[1]
                book_read_progress = lineInfo[2]
                # bookPath = lineInfo[3]
                book_nums = lineInfo[4]

                frame_book = QFrame()  # ???frame
                frame_book.setObjectName("frame_book")
                frame_image = QFrame_BookShelfImage(self.bookShelfLayoutNums, self.frame_noneBookShelf)  # ??????frame
                frame_image.setProperty("updating", "0")
                frame_image.setProperty("repairing", "0")
                serialNumber = lineInfo[13]
                frame_image.setProperty("serialNumber", serialNumber)
                frame_image.setProperty("frame_image_mask", None)
                frame_image.breakSignal_bookinfo_frame.connect(self.call_showBookInfo)
                frame_image.breakSignal_bookinfo_update_chapter.connect(self.call_update_chapter)
                frame_image.breakSignal_bookinfo_update_bookShelfLayout.connect(self.call_updateBookShelfLayout)
                frame_image.breakSignal_bookinfo_repair_chapter.connect(self.call_showBookChapterList)
                frame_image.breakSignal_bookinfo_lessBookNums.connect(self.call_lessBookShelfNums)
                frame_image.breakSignal_delBookInDownloadLayout.connect(self.call_delBookInDownloadLayout)
                vlayout_book = QVBoxLayout()  # ?????????
                vlayout_image = QVBoxLayout()  # ????????????
                btn_image = QPushButton_BookShelf()
                btn_image.breakSignal_showReader.connect(self.call_showReader)
                label_bookName = QLabel()
                label_name_metrics = QFontMetrics(QFont("Microsoft YaHei", 11))
                label_bookName.setText(label_name_metrics.elidedText(book_name, Qt.ElideRight, 110))

                label_bookProgress = QLabel(f"??????:{book_read_progress}%")

                frame_image.setLabelObject(label_bookProgress)

                btn_image.setMinimumSize(100, 150)
                btn_image.setMaximumSize(100, 150)

                btn_image.setObjectName(f"btn_bookshelf_image_{book_nums}")
                btn_image.setStyleSheet(f'''
                    border-image:url("{book_image_path}");
                    border:none;
                    ''')
                label_bookName.setFont(QFont("Microsoft YaHei", 11))
                label_bookName.setAlignment(Qt.AlignCenter)

                label_bookProgress.setFont(QFont("Microsoft YaHei", 9, QFont.Bold))
                label_bookProgress.setStyleSheet("color:#b2b2b2")
                label_bookProgress.setAlignment(Qt.AlignCenter)
                label_bookName.setContentsMargins(0, 0, 0, 0)
                label_bookProgress.setContentsMargins(0, 0, 0, 0)
                vlayout_book.setAlignment(Qt.AlignCenter)
                vlayout_book.setContentsMargins(0, 0, 0, 0)
                vlayout_image.addWidget(btn_image)
                frame_image.setLayout(vlayout_image)
                vlayout_image.setContentsMargins(0, 0, 0, 0)
                frame_image.setContentsMargins(1, 1, 1, 1)
                frame_image.setStyleSheet(
                    "border-radius: 6px;"
                    "border:2px solid #b2b2b2;"
                )
                vlayout_book.addWidget(frame_image)
                vlayout_book.addWidget(label_bookName)
                vlayout_book.addWidget(label_bookProgress)
                frame_book.setContentsMargins(0, 0, 0, 0)
                frame_book.setLayout(vlayout_book)
                frame_image.setContextMenuPolicy(Qt.CustomContextMenu)
                # frame_image.setContextMenuPolicy(3)
                frame_image.setMinimumSize(105, 155)
                frame_image.setMaximumSize(105, 155)
                frame_book.setMinimumSize(125, 250)
                frame_book.setMaximumSize(125, 250)
                log.info("???????????????%s" % str(frame_book))

                hlayout_bookshelf_line.addWidget(frame_book)
                hlayout_bookshelf_line.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                hlayout_bookshelf_line.setSpacing(120)
                frame_bookshelf_line.setContentsMargins(60, 0, 1260, 0)
                frame_bookshelf_line.setLayout(hlayout_bookshelf_line)
                self.vlayout_bookshelf_top.addWidget(frame_bookshelf_line)
                if is_row == len(bookshelflayoutinfo):
                    spaceItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
                    hlayout_bookshelf_line.addItem(spaceItem)

        else:
            self.frame_noneBookShelf.show()

    def initAddLineEditSearchBtn(self) -> None:  # ???????????????????????????????????????
        hlay = QHBoxLayout()
        self.btn_search_image = QPushButton()
        self.btn_search_image.setObjectName("btn_search_image")
        spaceItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.btn_search_image.setToolTip("??????")
        self.btn_search_image.setMinimumSize(25, 25)
        self.btn_search_image.setMaximumSize(25, 25)
        self.btn_search_image.setContentsMargins(0, 0, 0, 0)
        self.btn_search_image.clicked.connect(self.on_startSearchThreadEvent_clicked_returnPressed)  # ????????????????????????
        hlay.addItem(spaceItem)
        hlay.addWidget(self.btn_search_image)
        hlay.setAlignment(Qt.AlignCenter)
        hlay.setContentsMargins(0, 0, 6, 0)
        hlay.setSpacing(0)
        self.lineEdit_search.setStyleSheet("padding-right:28px;")
        self.lineEdit_search.setLayout(hlay)

    def initAddLineEditDebugSearchBtn(self) -> None:  # ????????????????????????????????????
        hlay = QHBoxLayout()
        self.btn_debug = QPushButton()
        self.btn_debug.setObjectName("btn_debug")
        spaceItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.btn_debug.setToolTip("Debug??????")
        self.btn_debug.setMinimumSize(25, 25)
        self.btn_debug.setMaximumSize(25, 25)
        self.btn_debug.setContentsMargins(0, 0, 0, 0)
        self.btn_debug.clicked.connect(self.on_startDebugThreadEvent_clicked)  # ????????????????????????
        hlay.addItem(spaceItem)
        hlay.addWidget(self.btn_debug)
        hlay.setAlignment(Qt.AlignCenter)
        hlay.setContentsMargins(0, 0, 6, 0)
        hlay.setSpacing(0)

        self.lineEdit_debugrule_search.setStyleSheet("padding-right:28px;")
        self.lineEdit_debugrule_search.setLayout(hlay)

    def initAddLabelSearchLoadingRefresh(self):  # ???????????????????????????????????????
        self.label_refresh_movie = QMovie(":/icon/icon/refresh.gif")
        self.label_refresh_movie.start()
        self.label_refresh.setMovie(self.label_refresh_movie)
        self.label_refresh.hide()

    def initAddNoneSearch(self) -> None:  # ??????????????????????????????
        self.frame_noneSearch = QFrame(self.scrollArea_searh_result_scrollAreaWidgetContents)
        vlayout_noneSearch = QVBoxLayout()
        btn_noneSearch = QPushButton()
        self.label_noneSearch = QLabel()

        self.label_noneSearch.setText("????????????????????????????????????!")
        self.label_noneSearch.setFont(QFont("Microsoft YaHei", 12))
        self.label_noneSearch.setAlignment(Qt.AlignCenter)
        btn_noneSearch.setStyleSheet(r'border-image:url(":/png/noneSearch.png");border-radius: 6px;')
        btn_noneSearch.setMinimumSize(QSize(400, 400))
        btn_noneSearch.setMaximumSize(QSize(400, 400))
        btn_noneSearch.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        vlayout_noneSearch.addWidget(btn_noneSearch)
        vlayout_noneSearch.addWidget(self.label_noneSearch)
        vlayout_noneSearch.setAlignment(Qt.AlignCenter)
        self.frame_noneSearch.setLayout(vlayout_noneSearch)
        self.frame_noneSearch.resize(btn_noneSearch.width(), btn_noneSearch.height())
        self.frame_noneSearch.setGeometry(
            220,
            50,
            self.frame_noneSearch.width(),
            self.frame_noneSearch.height()
        )
        self.frame_noneSearch.show()

    def initAddResponse(self) -> None:  # ?????????????????????url???response text???textedit??????
        self.textEdit_getUrl_getResult_response = QTextEdit_response_preview(self.frame_findtext,
                                                                             self.lineEdit_getUserFindText)
        self.textEdit_getUrl_getResult_response.setObjectName("textEdit_getUrl_getResult_response")
        self.textEdit_getUrl_getResult_preview = QTextEdit_response_preview(self.frame_findtext,
                                                                            self.lineEdit_getUserFindText)
        self.textEdit_getUrl_getResult_preview.setObjectName("textEdit_getUrl_getResult_preview")
        self.vlayout_response.addWidget(self.textEdit_getUrl_getResult_response)
        self.vlayout_preview.addWidget(self.textEdit_getUrl_getResult_preview)

        self.btn_getText_close.clicked.connect(lambda: self.frame_findtext.hide())
        self.btn_getText_pre.clicked.connect(self.on_getFindTextPre_clicked)
        self.btn_getText_next.clicked.connect(self.on_getFindTextNext_clicked)
        self.lineEdit_getUserFindText.returnPressed.connect(self.on_getFindTextNext_clicked)
        self.lineEdit_getUserFindText.textChanged.connect(self.on_setFindTextAllNums_textChanged)

        self.label_showFindTextNum = QLabel()
        self.label_showFindTextNum.setObjectName("label_showFindTextNum")
        self.label_showFindTextNum.setFont(QFont("Microsoft YaHei", 9))
        self.label_showFindTextNum.setText("0/0")
        self.hlayout_getUserFindText.addWidget(self.label_showFindTextNum)

    def initSearchLoading(self) -> None:  # ???????????????gif
        self.frame_loding = QFrame(self.scrollArea_searh_result_scrollAreaWidgetContents)
        label = QLabel(self.frame_loding)
        self.loding_movie = QMovie(QFileInfo("./Resource/loding_4.gif").absoluteFilePath())
        label.setMaximumSize(800, 600)
        label.setMinimumSize(800, 600)
        label.setMovie(self.loding_movie)
        label.setScaledContents(True)
        self.frame_loding.resize(label.width(), label.height())
        self.frame_loding.setGeometry(
            30, 0,
            label.width(), label.height()
        )
        self.frame_loding.hide()

    def insertBookShelfLayoutInfoSqlite(self,
                                        bookImage,
                                        bookName,
                                        bookProgress,
                                        bookPath,
                                        bookAuthor,
                                        bookStatus,
                                        bookLatestChapter,
                                        bookLatestUpdateTime,
                                        bookIntro,
                                        bookSourceName,
                                        bookUrl,
                                        bookRule,
                                        bookSerialNumber
                                        ) -> None:  # ?????????????????????????????????

        user = User.UserSql()
        selectInfo = user.selectBookShelfLayout()
        selectBookSerialNumber = user.selectBookShelfBookSerialNumber()
        selectBookNums = user.selectBookShelfMaxBookNum()
        bookNums = selectBookNums[0] + 1 if selectBookNums[0] is not None else 0
        if len(selectInfo) == 0:
            log.info(f"????????????????????????????????????????????????{bookName}")
            self.addBookShelfBook(bookImage, bookName, bookProgress, bookNums, selectInfo[0][13])
            user.insertBookShelfLayoutInfoSqlite(
                bookImage=bookImage,
                bookName=bookName,
                bookProgress=bookProgress,
                bookPath=bookPath,
                bookNums=bookNums,
                bookAuthor=bookAuthor,
                bookStatus=bookStatus,
                bookLatestChapter=bookLatestChapter,
                bookLatestUpdateTime=bookLatestUpdateTime,
                bookIntro=bookIntro,
                bookSourceName=bookSourceName,
                bookUrl=bookUrl,
                bookRule=bookRule,
                bookSerialNumber=bookSerialNumber
            )

        elif str(bookSerialNumber) in str(selectBookSerialNumber):
            QMessageBox_showMsg(text="???????????????????????????????????????").makeSure()
            log.info("?????????????????????????????????")
            log.info(f"??????????????????{self.bookShelfLayoutNums + 1}")
        else:
            log.info(f"???????????????????????????{bookName}")
            self.addBookShelfBook(bookImage, bookName, bookProgress, bookNums, selectInfo[0][13])
            user.insertBookShelfLayoutInfoSqlite(
                bookImage=bookImage,
                bookName=bookName,
                bookProgress=bookProgress,
                bookPath=bookPath,
                bookNums=bookNums,
                bookAuthor=bookAuthor,
                bookStatus=bookStatus,
                bookLatestChapter=bookLatestChapter,
                bookLatestUpdateTime=bookLatestUpdateTime,
                bookIntro=bookIntro,
                bookSourceName=bookSourceName,
                bookUrl=bookUrl,
                bookRule=bookRule,
                bookSerialNumber=bookSerialNumber
            )

    @staticmethod
    def insertReaderBookNormalInfo(currentPage: int,
                                   serialNumber: int,
                                   scrollTop: int):
        user = User.UserSql()
        user.insertReaderBookNormalInfo(currentPage=currentPage,
                                        serialNumber=serialNumber,
                                        scrollTop=scrollTop)

    @staticmethod
    def iteration_similar_property(search_result_control: list,
                                   this_similarity: float,
                                   that_property_key: str,
                                   sort_reverse: bool = True) -> int:  # ???????????????

        for i in range(len(search_result_control)):
            that_similarity = search_result_control[i].property(that_property_key)
            if sort_reverse:
                if this_similarity > that_similarity:
                    return i
            else:
                if this_similarity < that_similarity:
                    return i

    @staticmethod
    def insertDownloadLayoutInfoSqlite(taskBookImagePath,
                                       taskBookName,
                                       taskCreateTime,
                                       taskFinishTime,
                                       taskProgress,
                                       taskStatusInfo,
                                       taskBtnStatus,
                                       taskBookPath,
                                       taskLine,
                                       taskHomeUrl,
                                       taskWhichRule,
                                       taskProgressLabel,

                                       taskBookAuthor,
                                       taskBookStatus,
                                       taskBookIntro,
                                       taskBookSourceName,
                                       taskBookLatestChapter,
                                       taskLatestUpdateTime,
                                       taskSerialNumber: int  # ???????????????
                                       ):  # ????????????????????????????????????
        user = User.UserSql()
        user.insertDownloadLayoutInfo(
            taskBookImagePath=taskBookImagePath,
            taskBookName=taskBookName,
            taskCreateTime=taskCreateTime,
            taskFinishTime=taskFinishTime,
            taskProgress=taskProgress,
            taskStatusInfo=taskStatusInfo,
            taskBtnStatus=taskBtnStatus,
            taskBookPath=taskBookPath,
            taskLine=taskLine,
            taskHomeUrl=taskHomeUrl,
            taskWhichRule=taskWhichRule,
            taskProgressLabel=taskProgressLabel,

            taskBookAuthor=taskBookAuthor,
            taskBookStatus=taskBookStatus,
            taskBookIntro=taskBookIntro,
            taskBookSourceName=taskBookSourceName,
            taskBookLatestChapter=taskBookLatestChapter,
            taskLatestUpdateTime=taskLatestUpdateTime,
            taskSerialNumber=taskSerialNumber

        )

    def initDownloadRecording(self):  # ?????????????????????
        downloadlayoutinfo = self.getUserSqlLiteDownload()
        if downloadlayoutinfo:
            self.frame_noDownload.hide()
            for lineInfo in downloadlayoutinfo:
                imagePath = lineInfo[0]
                bookname = lineInfo[1]
                taskCreatTime = lineInfo[2]
                taskFinishTime = lineInfo[3]
                taskProgress = lineInfo[4]
                taskStatusInfo = lineInfo[5]
                taskBtnStatus = lineInfo[6]
                taskHomeUrl = lineInfo[9]
                taskWhichRule = lineInfo[10]
                taskProgressLabel = lineInfo[11]

                bookAuthor = lineInfo[12]  # ?????????
                bookStatus = lineInfo[13]  # ????????????
                bookIntro = lineInfo[14]  # ??????
                bookSourceName = lineInfo[15]  # ?????????
                bookLatestChapter = lineInfo[16]
                bookLatestUpdateTime = lineInfo[17]
                isTaskSerialNumber = lineInfo[18]
                self.call_addDownloadLayout(
                    bookAuthor=bookAuthor,  # ?????????
                    bookStatus=bookStatus,  # ????????????
                    bookIntro=bookIntro,  # ??????
                    bookSourceName=bookSourceName,  # ?????????
                    bookLatestChapter=bookLatestChapter,
                    bookLatestUpdateTime=bookLatestUpdateTime,

                    bookname=bookname,
                    imagePath=imagePath,
                    homeurl=taskHomeUrl,
                    whichRule=taskWhichRule,
                    taskCreatTime=taskCreatTime,
                    taskFinishTime=taskFinishTime,
                    taskProgress=taskProgress,
                    taskProgressLabel=taskProgressLabel,
                    taskBtnStatus=taskBtnStatus,  # ?????????????????????
                    taskStatusInfo=taskStatusInfo,
                    isTaskSerialNumber=isTaskSerialNumber,
                    task=False
                )

    def initNoDownloadRecording(self):  # ????????????????????????
        self.frame_noDownload = QFrame(self.stacked_download)
        self.frame_noDownload.setObjectName("frame_noDownload")
        vlayout = QVBoxLayout()

        label_image = QLabel()
        label_text = QLabel()
        pixmap = QPixmap(QFileInfo("./Resource/icon/noDownload.png").absoluteFilePath())
        label_image.setPixmap(pixmap)

        label_image.setMinimumSize(128, 128)
        label_image.setMaximumSize(128, 128)
        label_text.setText("??????????????????")
        label_text.setFont(QFont("Microsoft YaHei", 11))
        label_text.setAlignment(Qt.AlignCenter)
        self.frame_noDownload.setMinimumSize(128, 150)
        self.frame_noDownload.setMaximumSize(128, 150)

        vlayout.addWidget(label_image)
        vlayout.addWidget(label_text)
        vlayout.setContentsMargins(0, 0, 0, 0)
        self.frame_noDownload.setGeometry(409, 300, 128, 150)
        self.frame_noDownload.setLayout(vlayout)

    def initUserRuleLayout(self) -> None:  # ?????????????????????
        log.debug("???????????????????????????")

        for i in self.rule:
            self.addNewRuleLayout(bookSourceName=i["bookSourceName"], enable=i["enable"])

    def initPurifyRuleLayout(self) -> None:  # ???????????????????????????
        log.debug("?????????????????????????????????")
        for i in self.purify_rule:
            self.addNewPurifyLayout(purifySourceName=i["purifySourceName"], enable=i["enable"])

    def initXpathSetting(self):  # ?????????Xpath??????????????????
        self.btn_getUrl_implement.clicked.connect(self.on_threadXpath_clicked)
        self.btn_testXpath_implement.clicked.connect(self.on_threadXpathParseOne_clicked)
        self.lineEdit_testXpath_getText.returnPressed.connect(self.on_threadXpathParseOne_clicked)
        self.btn_testXpath_implement_two.clicked.connect(self.on_threadXpathParseTwo_clicked)
        self.btn_getUrl_getResult_response.clicked.connect(lambda: self.stackedWidget_getResult.setCurrentIndex(0))
        self.btn_getUrl_getResult_preview.clicked.connect(lambda: self.stackedWidget_getResult.setCurrentIndex(1))
        self.frame_findtext.hide()

    def initManageLocalSQLLayout(self):
        self.thread_init_manage_layout = QThread_SelectLocalSQLDatabase()
        self.thread_init_manage_layout.breakSignal_selectInfo.connect(self.call_updateManageLayout)
        self.thread_init_manage_layout.start()

    @staticmethod
    def Bytes_to_KBytes(Bytes) -> float:  # Bytes->Kb
        return round(Bytes / (1024), 2)

    @staticmethod
    def Bytes_to_MBytes(Bytes) -> float:  # Bytes->Mb
        return round(Bytes / pow(1024, 2), 2)

    def call_updateManageLayout(self, sql_info: list):
        log.info("???????????????????????????")
        for info in sql_info:
            serial_number = info[0]
            book_name = info[1]
            book_author = info[2]
            book_latest_chapter_name = info[3]
            book_url = info[4]
            book_chapter_nums = str(info[5])
            book_source_name = info[6]
            book_space_size = info[7]
            book_space_size = book_space_size * 3

            row_count = self.tableWidget_manage.rowCount()
            self.tableWidget_manage.insertRow(row_count)
            item = QTableWidgetItem()
            item_vertical = QTableWidgetItem()
            item_book_name = QTableWidgetItem()
            item_book_name.setText(book_name)
            item_book_author = QTableWidgetItem()
            item_book_latest_chapter_name = QTableWidgetItem()
            item_book_url = QTableWidgetItem()
            item_book_chapter_nums = QTableWidgetItem()
            item_book_source_name = QTableWidgetItem()
            item_book_space_size = QTableWidgetItem()

            item_vertical.setFont(QFont("Microsoft YaHei", 9))
            item_obj_list = [item_book_name, item_book_author, item_book_latest_chapter_name,
                             item_book_url, item_book_chapter_nums, item_book_source_name,
                             item_book_space_size]
            for item_ in item_obj_list:
                item_.setFont(QFont("Microsoft YaHei", 9))

            if ("????????????" == book_name) and ("????????????" == book_author) and ("????????????" == book_source_name):
                for item_ in item_obj_list:
                    item_.setForeground(QBrush(QColor(Qt.white)))
                    item_.setBackground(QBrush(QColor("#808080")))

            item.setCheckState(Qt.Unchecked)
            item_vertical.setText(str(serial_number))
            item_book_name.setText(book_name)
            item_book_author.setText(book_author)
            item_book_latest_chapter_name.setText(book_latest_chapter_name)
            item_book_url.setText(book_url)
            item_book_chapter_nums.setText(book_chapter_nums)
            item_book_source_name.setText(book_source_name)
            if book_space_size >= 1000000:
                book_space_size = str(self.Bytes_to_MBytes(Bytes=book_space_size)) + "MB"
            else:
                book_space_size = str(self.Bytes_to_KBytes(Bytes=book_space_size)) + "KB"
            item_book_space_size.setText(book_space_size)

            self.tableWidget_manage.setVerticalHeaderItem(row_count, item_vertical)
            self.tableWidget_manage.setItem(row_count, 0, item)
            self.tableWidget_manage.setItem(row_count, 1, item_book_name)
            self.tableWidget_manage.setItem(row_count, 2, item_book_author)
            self.tableWidget_manage.setItem(row_count, 3, item_book_latest_chapter_name)
            self.tableWidget_manage.setItem(row_count, 4, item_book_url)
            self.tableWidget_manage.setItem(row_count, 5, item_book_chapter_nums)
            self.tableWidget_manage.setItem(row_count, 6, item_book_source_name)
            self.tableWidget_manage.setItem(row_count, 7, item_book_space_size)

    def initCompleter(self):  # ???????????????????????????
        charset_list = ["utf-8", "gbk", "gb2312"]
        self.charset_ComboBox = QComboBox()
        self.charset_Completer = QCompleter(charset_list)
        self.charset_Completer.setFilterMode(Qt.MatchContains)
        self.charset_Completer.setCompletionMode(QCompleter.PopupCompletion)
        self.lineEdit_getUrl_charset.setCompleter(self.charset_Completer)

    def initCacheImagesEvent(self):  # ????????????????????????????????????
        self.thread_clear_cache_init = QThread_Calculate_Cache_Size()  # ?????????????????????
        self.thread_clear_cache_init.breakSignal_setLabel.connect(self.call_setCacheImagesLabel)
        self.thread_clear_cache_init.start()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # ?????????????????????????????????
            self.setCursor(QCursor(QPixmap(":/cursor/Cur/No_Disponible.cur"), 0, 0))

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if Qt.LeftButton and self.m_flag:
            self.move(event.globalPos() - self.m_Position)  # ??????????????????
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.m_flag = False
        self.setCursor(QCursor(QPixmap(":/cursor/Cur/normal.cur"), 0, 0))

    @staticmethod
    def saveUserData(a=None, b=None, c=None) -> None:
        user = User.UserSql()
        user.checkDefaultTable()  # ????????????????????????
        if a is not None and b is not None and c is not None:
            user.updateUserInfo(a, b, c)
        else:
            user.updateUserInfo()

    def update_self_rule(self):  # ????????????json?????????????????????self.rule
        log.info("????????????json?????????????????????self.rule")
        self.rule = regular.Json().getData()

    def update_self_purify_rule(self):  # ??????????????????json?????????????????????self.rule
        log.info("??????????????????json?????????????????????self.purify_rule")
        self.purify_rule = purify.Json().getData()


class QSystemTrayIcon_Background(QSystemTrayIcon):  # ??????
    def __init__(self, MainWindow, parent=None):
        super(QSystemTrayIcon_Background, self).__init__(parent)
        self.ui = MainWindow  # MainWindo????????????????????????????????????????????????????????????????????????
        self.createMenu()

    def createMenu(self) -> None:
        self.menu = QMenu()
        self.showAction1 = QAction(text=u"??????", parent=self)
        self.showAction1.triggered.connect(self.on_show_window_triggered)
        self.showAction2 = QAction(text=u"????????????", parent=self)
        self.showAction2.triggered.connect(self.on_showMsg_triggered)
        self.quitAction = QAction(text=u"??????", parent=self)
        self.quitAction.triggered.connect(self.on_quit_triggered)

        self.menu.addAction(self.showAction1)
        self.menu.addAction(self.showAction2)
        self.menu.addAction(self.quitAction)
        self.setContextMenu(self.menu)

        # ????????????
        self.setIcon(QIcon(os.getcwd() + "/Resource/favicon.ico"))
        self.icon = self.MessageIcon()

        # ??????????????????????????????????????????
        self.activated.connect(self.onIconClicked)

    def on_showMsg_triggered(self) -> None:
        self.showMessage("Message", "skr at here", self.icon)

    def on_show_window_triggered(self) -> None:
        # ????????????????????????????????????????????????????????????????????????????????????????????????
        self.ui.showNormal()
        self.ui.activateWindow()
        self.ui.setWindowFlags(Qt.FramelessWindowHint)
        self.ui.show()
        # self.ui.showNormal()
        # self.ui.activateWindow()

    @staticmethod
    def on_quit_triggered() -> None:
        # qApp.quit()
        sys.exit(app.exec_())

    # ????????????icon?????????????????????????????????????????????1????????????????????????2????????????3??????????????????4????????????????????????
    def onIconClicked(self, reason: int) -> None:
        if reason == 2 or reason == 3:
            # self.showMessage("Message", "skr at here", self.icon)
            if self.ui.isMinimized() or not self.ui.isVisible():
                # ????????????????????????????????????????????????????????????????????????????????????????????????
                self.ui.showNormal()
                self.ui.activateWindow()
                self.ui.setWindowFlags(Qt.FramelessWindowHint)
                self.ui.show()
            else:
                # ?????????????????????????????????
                self.ui.showMinimized()
                self.ui.setWindowFlags(Qt.SplashScreen)
                self.ui.show()


@atexit.register
def cleanUpRedundantSpace():
    log.info("???????????????????????????")
    user = User.UserSql()
    user.cleanUpRedundantSpace()
    try:
        os.kill(main_pid, signal.SIGINT)
    except OSError:
        log.info("??????????????????")


class QThread_BookInfo(QThread):
    def __init__(self, bookNums: int, serialNumber: int):
        super().__init__()
        self.serialNumber = serialNumber
        self.bookNums = bookNums
        self.del_status = False

    def run(self) -> None:
        user = User.UserSql()
        user.deleteBookShelfLayoutInfo(bookNums=self.bookNums)
        user.updateBookShelfLayoutInfo(bookNums=self.bookNums)
        if self.del_status:
            log.info("???????????????????????????")
            user.deleteIsInBookInfoDatabase(serialNumber=self.serialNumber)

    def setDelStatus(self, status: bool):
        self.del_status = status


def myExcepthook(ttype: type, tvalue: NameError, ttraceback):
    text_type_match = re.findall("'(.*)'", str(ttype))[0] if re.findall("'(.*)'", str(ttype)) else ttype
    text_type = f"class???    {text_type_match}\n"
    text_reason = f"reason???{tvalue}\n"
    text_file_match = re.findall("'(.*)'", str(ttraceback.tb_frame))[0] if re.findall("'(.*)'", str(
        ttraceback.tb_frame)) else "None"
    text_file = f"file???       {text_file_match}\n"
    text_line = f"lines???    {ttraceback.tb_lineno}\n"
    text = text_type + text_reason + text_file + text_line
    log.error("global error:\n%s" % text)
    QMessageBox_showMsg(title="?????????", icon="./Resource/errror.jpeg", text=text).makeSure()


if __name__ == '__main__':
    sys.excepthook = myExcepthook
    qInstallMessageHandler((lambda *args: None))  # ?????????????????????
    app = QApplication(sys.argv)
    window = Window()
    novel_rc  # ???????????????????????????
    window.show()
    sys.exit(app.exec_())
