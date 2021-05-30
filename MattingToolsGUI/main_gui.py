import os
import qtawesome
from PyQt5 import QtCore, QtWidgets, QtGui
from ui_thread import UI_Thread
import cv2
import numpy as np
import glob

# import ctypes
# ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('myappid')


class MainUI(QtWidgets.QMainWindow):

    def __init__(self, begin):
        super(MainUI, self).__init__()
        self.ismoving = False
        self.begin = begin
        self.origin_img_path = ''
        self.mask_img_path = ''
        self.mat_img_path = ''
        self.mat_cache_path = 'gui_utils/mat/'
        self.mask_cache_path = 'gui_utils/mask/'
        self.now_img = 'origin'
        self.setWindowIcon(QtGui.QIcon('gui_utils/pic/Tools.png'))
        self.setWindowTitle('Mating-Photo')
        self.setFixedSize(1300, 800)
        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QGridLayout()
        self.main_widget.setLayout(self.main_layout)
        self.left_widget = QtWidgets.QWidget(self)
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()
        self.left_widget.setStyleSheet(
            '\n            QPushButton{\n            border:none;\n            color:white;\n            }\n            QPushButton#left_label{\n                border:none;\n                border-bottom:1px solid white;\n                font-size:20px;\n                font-weight:700;\n                font-family: Microsoft YaHei UI;\n            }\n            QPushButton#left_button:hover{\n            border-left:4px solid red;\n            font-weight:700;\n            }\n            QWidget#left_widget{\n                background:gray;\n                border-bottom:1px solid white;\n                border-left:1px solid white;\n                border-bottom-left-radius:10px;\n                }\n        ')
        self.left_widget.setLayout(self.left_layout)
        self.button_widget = QtWidgets.QWidget(self)
        self.button_layout = QtWidgets.QGridLayout()
        self.button_widget.setObjectName('button_widget')
        self.button_widget.setLayout(self.button_layout)
        self.button_widget.setStyleSheet(
            '\n            QPushButton{\n                border:none;\n                color:white;\n            }\n            QWidget#button_widget{\n                background:gray;\n                border-top:1px solid white;\n                border-left:1px solid white;\n                border-top-left-radius:10px;\n                }\n            ')
        self.right_widget = QtWidgets.QWidget(self)
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setStyleSheet(
            '\n            QWidget#right_widget{\n                color:#232C51;\n                background:white;\n                border-top:1px solid darkGray;\n                border-bottom:1px solid darkGray;\n                border-right:1px solid darkGray;\n                border-top-right-radius:10px;\n                border-bottom-right-radius:10px;\n            }\n            QLabel#right_lable{\n                border:none;\n                font-size:16px;\n                font-weight:700;\n                font-family: Microsoft YaHei UI;\n            }\n        ')
        self.right_widget.setLayout(self.right_layout)
        self.main_layout.addWidget(self.left_widget, 2, 0, 11, 2)
        self.main_layout.addWidget(self.right_widget, 1, 2, 12, 10)
        self.main_layout.addWidget(self.button_widget, 1, 0, 1, 2)
        self.setCentralWidget(self.main_widget)
        self.setWindowOpacity(1)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.main_layout.setSpacing(0)
        self.mythread = UI_Thread()
        self.init_button()
        self.init_main_page()
        self.init_generating_table_page()
        self.init_table_query_page()

    def init_button(self):
        self.left_close = QtWidgets.QPushButton('×')
        self.left_close.clicked.connect(self.on_close_program)
        self.left_visit = QtWidgets.QPushButton('□')
        self.left_mini = QtWidgets.QPushButton('－')
        self.left_close.setFixedSize(20, 20)
        self.left_visit.setFixedSize(20, 20)
        self.left_mini.setFixedSize(20, 20)
        self.left_close.setStyleSheet(
            '\n            QPushButton{ \n                background:rgb(250,0,0);\n                border-radius:10px;\n                color:rgb(0,0,0);\n                font:bold 16px;\n                position:absolute;\n                text-align:center;\n                position:absolute;\n                left:50%;\n                top:50%;\n            }\n            QPushButton:hover{\n                background:rgb(128,0,0);\n            }\n            QPushButton:pressed{\n                background:rgb(255,0,0);\n            }\n            left:10px;\n            ')
        self.left_visit.setStyleSheet(
            '\n            QPushButton{\n                background:rgb(225,225,0);\n                border-radius:10px;\n                color:rgb(0,0,0);\n                font:bold 13px;\n                text-align:center;\n            }\n            QPushButton:hover{\n                background:rgb(128,128,0);\n            }\n            QPushButton:pressed{\n                background:rgb(255,255,0);\n            }\n        ')
        self.left_mini.setStyleSheet(
            '\n            QPushButton{\n                background:rgb(0,225,0);\n                border-radius:10px;\n                color:rgb(0,0,0);\n                font:bold 16px;\n                text-align:center;\n            }\n            QPushButton:hover{\n                background:green;\n            }\n            QPushButton:pressed{\n                background:rgb(0,255,0);\n            }\n        ')
        self.left_button_main_page = QtWidgets.QPushButton(qtawesome.icon(
            'fa.home', color='white', options=[{'scale_factor': 1.6}]), ' 首    页')
        self.left_button_main_page.setStyleSheet('font: 30px')
        self.left_button_main_page.setObjectName('left_button')
        self.left_button_main_page.clicked.connect(
            self.on_button_main_page_switch)
        self.left_button_generating_table = QtWidgets.QPushButton(qtawesome.icon(
            'fa.star', color='white', options=[{'scale_factor': 1.6}]), ' 选择原图')
        self.left_button_generating_table.setStyleSheet('font:30px')
        self.left_button_generating_table.setObjectName('left_button')
        self.left_button_generating_table.clicked.connect(
            self.on_button_generating_table_page_switch)
        self.left_button_searching_table = QtWidgets.QPushButton(qtawesome.icon(
            'fa.comment', color='white', options=[{'scale_factor': 1.6}]), ' 查看掩码')
        self.left_button_searching_table.setStyleSheet('font:30px')
        self.left_button_searching_table.setObjectName('left_button')
        self.left_button_searching_table.clicked.connect(
            self.on_button_query_page_switch)
        self.left_button_history_table = QtWidgets.QPushButton(qtawesome.icon(
            'fa.history', color='white', options=[{'scale_factor': 1.4}]), ' 查看抠图')
        self.left_button_history_table.setStyleSheet('font:30px')
        self.left_button_history_table.setObjectName('left_button')
        self.left_button_history_table.clicked.connect(self.on_check_matting)
        self.button_layout.addWidget(self.left_mini, 0, 2, 1, 1)
        self.button_layout.addWidget(self.left_visit, 0, 1, 1, 1)
        self.button_layout.addWidget(self.left_close, 0, 0, 1, 1)
        self.left_layout.addWidget(self.left_button_main_page, 2, 0, 1, 3)
        self.left_layout.addWidget(
            self.left_button_generating_table, 4, 0, 1, 3)
        self.left_layout.addWidget(
            self.left_button_searching_table, 5, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_history_table, 6, 0, 1, 3)

    def init_input_box(self):
        self.right_bar_widget = QtWidgets.QWidget()
        self.right_bar_layout = QtWidgets.QGridLayout()
        self.right_bar_widget.setLayout(self.right_bar_layout)
        self.right_layout.addWidget(self.right_bar_widget, 0, 0, 1, 9)

    def init_main_page(self):
        self.right_subwidgets = QtWidgets.QFrame()
        self.right_subwidgets_layout = QtWidgets.QGridLayout()
        self.right_subwidgets.setLayout(self.right_subwidgets_layout)
        self.img = QtGui.QPixmap('gui_utils/pic/2.png')
        print(self.img.size())
        self.img_label = QtWidgets.QLabel()
        self.img_label.setObjectName('img_label')
        self.img_label.setPixmap(self.img)
        self.img_label.setStyleSheet(
            '\n            QLabel{\n                margin-bottom: 200px;\n            }\n        ')
        self.about_button = QtWidgets.QPushButton('关于我们')
        self.about_button.setObjectName('about_button')
        self.about_button.setStyleSheet(
            '\n            QPushButton#about_button {\n                width: 20px;\n                height: 40px;\n                background-color: gray;\n                border: 3px solid gray;\n                border-radius: 5px;\n                color: white;\n                font-family: Microsoft YaHei UI;\n                font-size: 25px;\n            }\n            QPushButton#about_button:hover{\n                width: 20px;\n                height: 40px;\n                background-color: rgb(65,65,65);\n                border: 3px solid gray;\n                border-radius: 5px;\n                border-color: rgb(65,65,65);\n                color: white;\n                font-family: Microsoft YaHei UI;\n            }\n            QPushButton#about_button:pressed{\n                width: 20px;\n                height: 40px;\n                background-color: rgb(1,1,1);\n                border: 3px solid gray;\n                border-radius: 5px;\n                border-color: rgb(1,1,1);\n                color: white;\n                font-family: Microsoft YaHei UI;\n            }\n        ')
        self.about_button.clicked.connect(self.on_about_msg_box)
        self.introduction_background = QtWidgets.QLabel()
        self.introduction_background.setObjectName('introduction_background')
        self.right_subwidgets_layout.addWidget(self.img_label, 1, 0, 1, 5)
        self.right_subwidgets_layout.addWidget(self.about_button, 4, 4, 1, 1)
        self.right_layout.addWidget(self.right_subwidgets, 0, 0, 1, 9)

    def init_generating_table_page(self):
        self.right_bar_widget = QtWidgets.QFrame()
        self.right_bar_layout = QtWidgets.QGridLayout()
        self.right_bar_widget.setLayout(self.right_bar_layout)
        self.img_origin = QtGui.QPixmap(self.origin_img_path)
        self.img_origin_label = QtWidgets.QLabel()
        self.img_origin_label.setPixmap(self.img_origin)
        self.img_origin_label.setObjectName('img_origin_label')
        self.img_origin_label.setAlignment(QtCore.Qt.AlignCenter)
        self.img_origin_label.setStyleSheet(
            '\n            margin-top:20px;\n        ')
        self.right_bar_layout.addWidget(self.img_origin_label, 3, 3, 1, 5)
        self.box_layout = QtWidgets.QHBoxLayout()
        self.import_factor_button = QtWidgets.QPushButton('选择图像')
        self.import_factor_button.setObjectName('import_button')
        self.import_factor_button.clicked.connect(self.on_import_factor_button)
        self.export_sample_button = QtWidgets.QPushButton('开始推理')
        self.export_sample_button.setObjectName('export_button')
        self.export_sample_button.clicked.connect(self.on_export_sample_button)
        self.begin_button = QtWidgets.QPushButton('滤镜')
        self.begin_button.setObjectName('import_button')
        self.begin_button.clicked.connect(self.on_begin_button)
        self.more_photo = QtWidgets.QPushButton('批量推理')
        self.more_photo.setObjectName('import_button')
        self.more_photo.clicked.connect(self.on_more_photo)
        self.import_factor_button.setStyleSheet(
            '\n            QPushButton#import_button{\n                width: 20px;\n                height: 40px;\n                background-color: gray;\n                border: 3px solid gray;\n                border-radius: 5px;\n                color: white;\n                font-family: Microsoft YaHei UI;\n                font-size: 25px;\n            }\n            QPushButton#import_button:hover{\n                width: 20px;\n                height: 40px;\n                background-color: rgb(65,65,65);\n                border: 3px solid gray;\n                border-radius: 5px;\n                border-color: rgb(65,65,65);\n                color: white;\n                font-family: Microsoft YaHei UI;\n            }\n            QPushButton#import_button:pressed{\n                width: 20px;\n                height: 40px;\n                background-color: rgb(1,1,1);\n                border: 3px solid gray;\n                border-radius: 5px;\n                border-color: rgb(1,1,1);\n                color: white;\n                font-family: Microsoft YaHei UI;\n            }\n        ')
        self.export_sample_button.setStyleSheet(
            '\n            QPushButton#export_button{\n                width: 20px;\n                height: 40px;\n                background-color: gray;\n                border: 3px solid gray;\n                border-radius: 5px;\n                color: white;\n                font-family: Microsoft YaHei UI;\n                font-size: 25px;\n            }\n            QPushButton#export_button:hover{\n                width: 20px;\n                height: 40px;\n                background-color: rgb(65,65,65);\n                border: 3px solid gray;\n                border-radius: 5px;\n                border-color: rgb(65,65,65);\n                color: white;\n                font-family: Microsoft YaHei UI;\n            }\n            QPushButton#export_button:pressed{\n                width: 20px;\n                height: 40px;\n                background-color: rgb(1,1,1);\n                border: 3px solid gray;\n                border-radius: 5px;\n                border-color: rgb(1,1,1);\n                color: white;\n                font-family: Microsoft YaHei UI;\n            }\n        ')
        self.begin_button.setStyleSheet(
            '\n                    QPushButton#import_button{\n                        width: 20px;\n                        height: 40px;\n                        background-color: gray;\n                        border: 3px solid gray;\n                        border-radius: 5px;\n                        color: white;\n                        font-family: Microsoft YaHei UI;\n                        font-size: 25px;\n                    }\n                    QPushButton#import_button:hover{\n                        width: 20px;\n                        height: 40px;\n                        background-color: rgb(65,65,65);\n                        border: 3px solid gray;\n                        border-radius: 5px;\n                        border-color: rgb(65,65,65);\n                        color: white;\n                        font-family: Microsoft YaHei UI;\n                    }\n                    QPushButton#import_button:pressed{\n                        width: 20px;\n                        height: 40px;\n                        background-color: rgb(1,1,1);\n                        border: 3px solid gray;\n                        border-radius: 5px;\n                        border-color: rgb(1,1,1);\n                        color: white;\n                        font-family: Microsoft YaHei UI;\n                    }\n                ')
        self.more_photo.setStyleSheet(
            '\n                    QPushButton#import_button{\n                        width: 20px;\n                        height: 40px;\n                        background-color: gray;\n                        border: 3px solid gray;\n                        border-radius: 5px;\n                        color: white;\n                        font-family: Microsoft YaHei UI;\n                        font-size: 25px;\n                    }\n                    QPushButton#import_button:hover{\n                        width: 20px;\n                        height: 40px;\n                        background-color: rgb(65,65,65);\n                        border: 3px solid gray;\n                        border-radius: 5px;\n                        border-color: rgb(65,65,65);\n                        color: white;\n                        font-family: Microsoft YaHei UI;\n                    }\n                    QPushButton#import_button:pressed{\n                        width: 20px;\n                        height: 40px;\n                        background-color: rgb(1,1,1);\n                        border: 3px solid gray;\n                        border-radius: 5px;\n                        border-color: rgb(1,1,1);\n                        color: white;\n                        font-family: Microsoft YaHei UI;\n                    }\n                ')
        self.right_bar_layout.addWidget(self.import_factor_button, 1, 3, 1, 1)
        self.right_bar_layout.addWidget(self.export_sample_button, 1, 4, 1, 1)
        self.right_bar_layout.addWidget(self.begin_button, 1, 5, 1, 1)
        self.right_bar_layout.addWidget(self.more_photo, 1, 6, 1, 1)
        self.right_layout.addWidget(self.right_bar_widget, 0, 0, 0, 10)
        self.right_bar_widget.setVisible(False)

    def init_table_query_page(self):
        self.right_query_widget = QtWidgets.QFrame()
        self.right_query_layout = QtWidgets.QGridLayout()
        self.right_layout.addWidget(self.right_query_widget, 0, 0, 1, 9)
        self.right_query_widget.setVisible(False)

    def on_button_generating_table_page_switch(self):
        self.right_bar_widget.setVisible(True)
        self.right_query_widget.setVisible(False)
        self.right_subwidgets.setVisible(False)
        if self.origin_img_path:
            temp = QtGui.QPixmap(self.origin_img_path)
            w, h = self.caculate_resize(temp.width(), temp.height())
            temp = temp.scaled(w, h)
            self.img_origin_label.setPixmap(temp)
        self.now_img = 'origin'

    def on_button_main_page_switch(self):
        self.right_bar_widget.setVisible(False)
        self.right_query_widget.setVisible(False)
        self.right_subwidgets.setVisible(True)

    def on_button_query_page_switch(self):
        if self.mask_img_path:
            temp = QtGui.QPixmap(self.mask_img_path)
            w, h = self.caculate_resize(temp.width(), temp.height())
            temp = temp.scaled(w, h)
            self.img_origin_label.setPixmap(temp)
            self.now_img = 'mask'
        else:
            self.choose_error = QtWidgets.QMessageBox()
            self.choose_error.setWindowTitle('未选择原图！')
            self.choose_error.setText('未选择原图！请先选择原图！\n')
            confirm_button = QtWidgets.QPushButton('确定')
            confirm_button.setStyleSheet(
                '\n                                               QPushButton{\n                                                   width: 60px;\n                                                   height: 30px;\n                                                   background-color: gray;\n                                                   border: 3px solid gray;\n                                                   border-radius: 5px;\n                                                   color: white;\n                                                   font-family: Microsoft YaHei UI;\n                                                   font-size:20px;\n                                               }\n                                               QPushButton:hover{\n                                                   background-color: rgb(65,65,65);\n                                                   border: 3px solid gray;\n                                                   border-radius: 5px;\n                                                   border-color: rgb(65,65,65);\n                                                   color: white;\n                                                   font-family: Microsoft YaHei UI;\n                                               }\n                                               QPushButton:pressed{\n                                                   background-color: rgb(1,1,1);\n                                                   border: 3px solid gray;\n                                                   border-radius: 5px;\n                                                   border-color: rgb(1,1,1);\n                                                   color: white;\n                                                   font-family: Microsoft YaHei UI;\n                                               }\n                                           ')
            self.choose_error.addButton(
                confirm_button, QtWidgets.QMessageBox.YesRole)
            self.choose_error.setStyleSheet(
                '\n                                               QMessageBox {\n                                                   font-family:Microsoft YaHei UI;\n                                                   font-size:18px;\n                                                   background-color:white; \n                                                   border:5px solid gray;\n                                                   border-radius:10px;\n                                               }\n                                           ')
            self.choose_error.setWindowFlag(QtCore.Qt.FramelessWindowHint)
            self.choose_error.exec_()

    def on_check_matting(self):
        if self.mat_img_path:
            temp = QtGui.QPixmap(self.mat_img_path)
            w, h = self.caculate_resize(temp.width(), temp.height())
            temp = temp.scaled(w, h)
            self.img_origin_label.setPixmap(temp)
            self.now_img = 'mat'
        else:
            self.choose_error = QtWidgets.QMessageBox()
            self.choose_error.setWindowTitle('未选择原图！')
            self.choose_error.setText('未选择原图！请先选择原图！\n')
            confirm_button = QtWidgets.QPushButton('确定')
            confirm_button.setStyleSheet(
                '\n                                                           QPushButton{\n                                                               width: 60px;\n                                                               height: 30px;\n                                                               background-color: gray;\n                                                               border: 3px solid gray;\n                                                               border-radius: 5px;\n                                                               color: white;\n                                                               font-family: Microsoft YaHei UI;\n                                                               font-size:20px;\n                                                           }\n                                                           QPushButton:hover{\n                                                               background-color: rgb(65,65,65);\n                                                               border: 3px solid gray;\n                                                               border-radius: 5px;\n                                                               border-color: rgb(65,65,65);\n                                                               color: white;\n                                                               font-family: Microsoft YaHei UI;\n                                                           }\n                                                           QPushButton:pressed{\n                                                               background-color: rgb(1,1,1);\n                                                               border: 3px solid gray;\n                                                               border-radius: 5px;\n                                                               border-color: rgb(1,1,1);\n                                                               color: white;\n                                                               font-family: Microsoft YaHei UI;\n                                                           }\n                                                       ')
            self.choose_error.addButton(
                confirm_button, QtWidgets.QMessageBox.YesRole)
            self.choose_error.setStyleSheet(
                '\n                                                           QMessageBox {\n                                                               font-family:Microsoft YaHei UI;\n                                                               font-size:18px;\n                                                               background-color:white;\n                                                               border:5px solid gray;\n                                                               border-radius:10px;\n                                                           }\n                                                       ')
            self.choose_error.setWindowFlag(QtCore.Qt.FramelessWindowHint)
            self.choose_error.exec_()

    def on_button_reset_input_box(self):
        self.factor_box.setPlainText('')
        self.output_box.setPlainText('')

    def error_msg_box(self):
        self.error_msgbox = QtWidgets.QMessageBox()
        self.error_msgbox.setWindowTitle('错误')
        self.error_msgbox.setText('输入格式有误，请重新输入！！')
        confirm_button = QtWidgets.QPushButton('确定')
        cancle_button = QtWidgets.QPushButton('取消')
        confirm_button.setStyleSheet(
            '\n            QPushButton{\n                width: 60px;\n                height: 30px;\n                background-color: gray;\n                border: 3px solid gray;\n                border-radius: 5px;\n                color: white;\n                font-family: Microsoft YaHei UI;\n                font-size:20px;\n            }\n            QPushButton:hover{\n                background-color: rgb(65,65,65);\n                border: 3px solid gray;\n                border-radius: 5px;\n                border-color: rgb(65,65,65);\n                color: white;\n                font-family: Microsoft YaHei UI;\n            }\n            QPushButton:pressed{\n                background-color: rgb(1,1,1);\n                border: 3px solid gray;\n                border-radius: 5px;\n                border-color: rgb(1,1,1);\n                color: white;\n                font-family: Microsoft YaHei UI;\n            }\n        ')
        cancle_button.setStyleSheet(
            '\n            QPushButton{\n                width: 60px;\n                height: 30px;\n                background-color: gray;\n                border: 3px solid gray;\n                border-radius: 5px;\n                color: white;\n                font-family: Microsoft YaHei UI;\n                font-size:20px;\n            }\n            QPushButton:hover{\n                background-color: rgb(65,65,65);\n                border: 3px solid gray;\n                border-radius: 5px;\n                border-color: rgb(65,65,65);\n                color: white;\n                font-family: Microsoft YaHei UI;\n            }\n            QPushButton:pressed{\n                background-color: rgb(1,1,1);\n                border: 3px solid gray;\n                border-radius: 5px;\n                border-color: rgb(1,1,1);\n                color: white;\n                font-family: Microsoft YaHei UI;\n            }\n        ')
        self.error_msgbox.addButton(
            confirm_button, QtWidgets.QMessageBox.YesRole)
        self.error_msgbox.addButton(
            cancle_button, QtWidgets.QMessageBox.NoRole)
        self.error_msgbox.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.error_msgbox.setStyleSheet(
            '\n            QMessageBox{\n                font-family:Microsoft YaHei UI;\n                font-size:25px;\n                background-color:white;\n                border:5px solid gray;\n                border-radius:10px;\n            }\n        ')
        self.error_msgbox.exec_()
        if self.error_msgbox == QtWidgets.QMessageBox.Yes:
            self.on_button_reset_input_box()
        else:
            if self.error_msgbox == QtWidgets.QMessageBox.No:
                self.on_button_reset_input_box()
            else:
                self.on_button_reset_input_box()

    def empty_msg_box(self):
        self.empty_msgbox = QtWidgets.QMessageBox()
        self.empty_msgbox.setWindowTitle('错误')
        self.empty_msgbox.setText('水平因素框输入为空，请重新输入！！')
        confirm_button = QtWidgets.QPushButton('确定')
        cancle_button = QtWidgets.QPushButton('取消')
        confirm_button.setStyleSheet(
            '\n            QPushButton{\n                background-color: gray;\n                border: 3px solid gray;\n                border-radius: 5px;\n                color: white;\n                font-family: Microsoft YaHei UI;\n                font-size:25px;\n            }\n            QPushButton:hover{\n                background-color: rgb(65,65,65);\n                border: 3px solid gray;\n                border-radius: 5px;\n                border-color: rgb(65,65,65);\n                color: white;\n                font-family: Microsoft YaHei UI;\n            }\n            QPushButton:pressed{\n                background-color: rgb(1,1,1);\n                border: 3px solid gray;\n                border-radius: 5px;\n                border-color: rgb(1,1,1);\n                color: white;\n                font-family: Microsoft YaHei UI;\n            }\n        ')
        cancle_button.setStyleSheet(
            '\n            QPushButton{\n                background-color: gray;\n                border: 3px solid gray;\n                border-radius: 5px;\n                color: white;\n                font-family: Microsoft YaHei UI;\n                font-size:25px;\n            }\n            QPushButton:hover{\n                background-color: rgb(65,65,65);\n                border: 3px solid gray;\n                border-radius: 5px;\n                border-color: rgb(65,65,65);\n                color: white;\n                font-family: Microsoft YaHei UI;\n            }\n            QPushButton:pressed{\n                background-color: rgb(1,1,1);\n                border: 3px solid gray;\n                border-radius: 5px;\n                border-color: rgb(1,1,1);\n                color: white;\n                font-family: Microsoft YaHei UI;\n            }\n        ')
        self.empty_msgbox.addButton(
            confirm_button, QtWidgets.QMessageBox.YesRole)
        self.empty_msgbox.addButton(
            cancle_button, QtWidgets.QMessageBox.NoRole)
        self.empty_msgbox.setStyleSheet(
            '\n            QMessageBox{\n                font-family:Microsoft YaHei UI;\n                font-size:25px;\n                background-color:white;\n                border:5px solid gray;\n                border-radius:10px;\n            }\n        ')
        self.empty_msgbox.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.empty_msgbox.exec_()
        if self.empty_msgbox == QtWidgets.QMessageBox.Yes:
            self.on_button_reset_input_box()
        else:
            if self.empty_msgbox == QtWidgets.QMessageBox.Cancel:
                self.on_button_reset_input_box()
            else:
                self.on_button_reset_input_box()

    def not_found_msg_box(self):
        self.not_found_msgbox = QtWidgets.QMessageBox()
        self.not_found_msgbox.setWindowTitle('错误')
        self.not_found_msgbox.setText('输入的水平^因素数错误，未在正交表中找到，请重新输入！！')
        confirm_button = QtWidgets.QPushButton('确定')
        cancle_button = QtWidgets.QPushButton('取消')
        confirm_button.setStyleSheet(
            '\n            QPushButton{\n                background-color: gray;\n                border: 3px solid gray;\n                border-radius: 5px;\n                color: white;\n                font-family: Microsoft YaHei UI;\n                font-size:25px;\n            }\n            QPushButton:hover{\n                background-color: rgb(65,65,65);\n                border: 3px solid gray;\n                border-radius: 5px;\n                border-color: rgb(65,65,65);\n                color: white;\n                font-family: Microsoft YaHei UI;\n            }\n            QPushButton:pressed{\n                background-color: rgb(1,1,1);\n                border: 3px solid gray;\n                border-radius: 5px;\n                border-color: rgb(1,1,1);\n                color: white;\n                font-family: Microsoft YaHei UI;\n            }\n        ')
        cancle_button.setStyleSheet(
            '\n            QPushButton{\n                background-color: gray;\n                border: 3px solid gray;\n                border-radius: 5px;\n                color: white;\n                font-family: Microsoft YaHei UI;\n                font-size:25px;\n            }\n            QPushButton:hover{\n                background-color: rgb(65,65,65);\n                border: 3px solid gray;\n                border-radius: 5px;\n                border-color: rgb(65,65,65);\n                color: white;\n                font-family: Microsoft YaHei UI;\n            }\n            QPushButton:pressed{\n                background-color: rgb(1,1,1);\n                border: 3px solid gray;\n                border-radius: 5px;\n                border-color: rgb(1,1,1);\n                color: white;\n                font-family: Microsoft YaHei UI;\n            }\n        ')
        self.not_found_msgbox.addButton(
            confirm_button, QtWidgets.QMessageBox.YesRole)
        self.not_found_msgbox.addButton(
            cancle_button, QtWidgets.QMessageBox.NoRole)
        self.not_found_msgbox.setStyleSheet(
            '\n            QMessageBox{\n                font-family:Microsoft YaHei UI;\n                font-size:25px;\n                background-color:white;\n                border:5px solid gray;\n                border-radius:10px;\n            }\n        ')
        self.not_found_msgbox.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.not_found_msgbox.exec_()
        if self.not_found_msgbox == QtWidgets.QMessageBox.Yes:
            self.on_button_reset_input_box()
        else:
            if self.not_found_msgbox == QtWidgets.QMessageBox.Cancel:
                self.on_button_reset_input_box()
            else:
                self.on_button_reset_input_box()

    def error_format_msg_box(self):
        self.error_format_msgbox = QtWidgets.QMessageBox()
        self.error_format_msgbox.setWindowTitle('错误')
        self.error_format_msgbox.setText('输入的因素和水平数与水平^因素框中的不符，请重新输入！！')
        confirm_button = QtWidgets.QPushButton('确定')
        cancle_button = QtWidgets.QPushButton('取消')
        confirm_button.setStyleSheet(
            '\n            QPushButton{\n                background-color: gray;\n                border: 3px solid gray;\n                border-radius: 5px;\n                color: white;\n                font-family: Microsoft YaHei UI;\n                font-size:25px;\n            }\n            QPushButton:hover{\n                background-color: rgb(65,65,65);\n                border: 3px solid gray;\n                border-radius: 5px;\n                border-color: rgb(65,65,65);\n                color: white;\n                font-family: Microsoft YaHei UI;\n            }\n            QPushButton:pressed{\n                background-color: rgb(1,1,1);\n                border: 3px solid gray;\n                border-radius: 5px;\n                border-color: rgb(1,1,1);\n                color: white;\n                font-family: Microsoft YaHei UI;\n            }\n        ')
        cancle_button.setStyleSheet(
            '\n            QPushButton{\n                background-color: gray;\n                border: 3px solid gray;\n                border-radius: 5px;\n                color: white;\n                font-family: Microsoft YaHei UI;\n                font-size:25px;\n            }\n            QPushButton:hover{\n                background-color: rgb(65,65,65);\n                border: 3px solid gray;\n                border-radius: 5px;\n                border-color: rgb(65,65,65);\n                color: white;\n                font-family: Microsoft YaHei UI;\n            }\n            QPushButton:pressed{\n                background-color: rgb(1,1,1);\n                border: 3px solid gray;\n                border-radius: 5px;\n                border-color: rgb(1,1,1);\n                color: white;\n                font-family: Microsoft YaHei UI;\n            }\n        ')
        self.error_format_msgbox.addButton(
            confirm_button, QtWidgets.QMessageBox.YesRole)
        self.error_format_msgbox.addButton(
            cancle_button, QtWidgets.QMessageBox.NoRole)
        self.error_format_msgbox.setStyleSheet(
            '\n            QMessageBox{\n                font-family:Microsoft YaHei UI;\n                font-size:25px;\n                background-color:white;\n                border:5px solid gray;\n                border-radius:10px;\n            }\n        ')
        self.error_format_msgbox.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.error_format_msgbox.exec_()
        if self.error_format_msgbox == QtWidgets.QMessageBox.Yes:
            self.on_button_reset_input_box()
        else:
            if self.error_format_msgbox == QtWidgets.QMessageBox.Cancel:
                self.on_button_reset_input_box()
                return
            self.on_button_reset_input_box()

    def export_error_msg_box(self):
        self.error_format_msgbox = QtWidgets.QMessageBox()
        self.error_format_msgbox.setWindowTitle('错误')
        self.error_format_msgbox.setText('当前输出框为空，无法导出！！')
        confirm_button = QtWidgets.QPushButton('确定')
        cancle_button = QtWidgets.QPushButton('取消')
        confirm_button.setStyleSheet(
            '\n            QPushButton{\n                width: 60px;\n                height: 30px;\n                background-color: gray;\n                border: 3px solid gray;\n                border-radius: 5px;\n                color: white;\n                font-family: Microsoft YaHei UI;\n                font-size:20px;\n            }\n            QPushButton:hover{\n                background-color: rgb(65,65,65);\n                border: 3px solid gray;\n                border-radius: 5px;\n                border-color: rgb(65,65,65);\n                color: white;\n                font-family: Microsoft YaHei UI;\n            }\n            QPushButton:pressed{\n                background-color: rgb(1,1,1);\n                border: 3px solid gray;\n                border-radius: 5px;\n                border-color: rgb(1,1,1);\n                color: white;\n                font-family: Microsoft YaHei UI;\n            }\n        ')
        cancle_button.setStyleSheet(
            '\n            QPushButton{\n                width: 60px;\n                height: 30px;\n                background-color: gray;\n                border: 3px solid gray;\n                border-radius: 5px;\n                color: white;\n                font-family: Microsoft YaHei UI;\n                font-size:20px;\n            }\n            QPushButton:hover{\n                background-color: rgb(65,65,65);\n                border: 3px solid gray;\n                border-radius: 5px;\n                border-color: rgb(65,65,65);\n                color: white;\n                font-family: Microsoft YaHei UI;\n            }\n            QPushButton:pressed{\n                background-color: rgb(1,1,1);\n                border: 3px solid gray;\n                border-radius: 5px;\n                border-color: rgb(1,1,1);\n                color: white;\n                font-family: Microsoft YaHei UI;\n            }\n        ')
        self.error_format_msgbox.addButton(
            confirm_button, QtWidgets.QMessageBox.YesRole)
        self.error_format_msgbox.addButton(
            cancle_button, QtWidgets.QMessageBox.NoRole)
        self.error_format_msgbox.setStyleSheet(
            '\n            QMessageBox{\n                font-family:Microsoft YaHei UI;\n                font-size:25px;\n                background-color:white;\n                border:5px solid gray;\n                border-radius:10px;\n            }\n        ')
        self.error_format_msgbox.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.error_format_msgbox.exec_()

    def find_factor_num_in_table(self, factor_num_str, table):
        result = []
        self.formated_list = []
        factor_num_str_splited = factor_num_str.split('^')
        for str_splited in factor_num_str_splited:
            if len(str_splited) > 1:
                str_splited = str_splited.split(' ')
                for _str in str_splited:
                    self.formated_list.append(_str)

                continue
            self.formated_list.append(str_splited)

        print(self.formated_list)
        if self.formated_list[1] == '':
            self.error_format_msg_box()
            return
        input_level_num = int(self.formated_list[0])
        input_factor_num = int(self.formated_list[1])
        for index, line in enumerate(table):
            if '^' in line:
                table_len = int(line.split(
                    ' ')[(-1)].split('\n')[0].split('n=')[(-1)])
                self.table_len = table_len
                table_factor_num = line.split(' ')[0]
                self.level_num = int(table_factor_num.split('^')[0])
                self.factor_num = int(table_factor_num.split('^')[1])
                if input_level_num == self.level_num and input_factor_num == self.factor_num:
                    for i in range(index + 1, index + table_len + 1):
                        result.append(table[i].split('\n')[0])

                    break

        if len(result) == 0:
            return
        return result

    def on_network_testing(self):
        self.mythread.start()
        address = 'baidu.com'
        print('正在尝试连接' + address + '...')
        _str = os.popen('ping ' + address)
        self.network_status_msg_box(_str.read())

    def on_close_program(self):
        app = QtWidgets.QApplication.instance()
        app.quit()

    def on_minmize_window(self):
        self.main_widget.setWindowState(QtCore.Qt.WindowMinimized)

    def on_maxmize_window(self):
        self.main_widget.setWindowState(QtCore.Qt.WindowMaximized)

    def on_about_msg_box(self):
        self.about_button_msgbox = QtWidgets.QMessageBox()
        self.about_button_msgbox.setWindowTitle('错误')
        self.about_button_msgbox.setText(
            '\n       欢迎您使用此工具！此工具由Have hands团队开发，可以将用户选择的图片进行非特定类型的前景主体分割，并生成mask和抠图结果。\n\n\n\n\nHave hands团队\t\nEmail:zeorainssakura@qq.com\t\nTencentQQ: 2274033547')
        confirm_button = QtWidgets.QPushButton('确定')
        confirm_button.setStyleSheet(
            '\n            QPushButton{\n                width: 60px;\n                height: 30px;\n                background-color: gray;\n                border: 3px solid gray;\n                border-radius: 5px;\n                color: white;\n                font-family: Microsoft YaHei UI;\n                font-size:20px;\n            }\n            QPushButton:hover{\n                background-color: rgb(65,65,65);\n                border: 3px solid gray;\n                border-radius: 5px;\n                border-color: rgb(65,65,65);\n                color: white;\n                font-family: Microsoft YaHei UI;\n            }\n            QPushButton:pressed{\n                background-color: rgb(1,1,1);\n                border: 3px solid gray;\n                border-radius: 5px;\n                border-color: rgb(1,1,1);\n                color: white;\n                font-family: Microsoft YaHei UI;\n            }\n        ')
        self.about_button_msgbox.addButton(
            confirm_button, QtWidgets.QMessageBox.YesRole)
        self.about_button_msgbox.setStyleSheet(
            '\n            QMessageBox {\n                font-family:Microsoft YaHei UI;\n                font-size:18px;\n                background-color:white;\n                border:5px solid gray;\n                border-radius:10px;\n            }\n        ')
        self.about_button_msgbox.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.about_button_msgbox.exec_()

    def on_more_photo(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "getExistingDirectory", "./")
        img_list = glob.glob(directory+os.sep+"*.*")
        for img_path in img_list:
            self.origin_img_path = img_path.replace("\\",'/')
            self.begin.path = self.origin_img_path
            self.mask_img_path = ''
            self.mat_img_path = ''
            self.begin.run()
            mask_img_path = self.begin.mask_total_path
            mat_img_path = self.begin.mat_total_path
            self.infer_error = QtWidgets.QMessageBox()
            self.infer_error.setWindowTitle('推理成功！')
            self.infer_error.setText(
                '图像推理成功！本次推理用时：%.3fs   \n' % self.begin.time_run)
            confirm_button = QtWidgets.QPushButton('确定')
            confirm_button.setStyleSheet(
                '\n                                    QPushButton{\n                                        width: 60px;\n                                        height: 30px;\n                                        background-color: gray;\n                                        border: 3px solid gray;\n                                        border-radius: 5px;\n                                        color: white;\n                                        font-family: Microsoft YaHei UI;\n                                        font-size:20px;\n                                    }\n                                    QPushButton:hover{\n                                        background-color: rgb(65,65,65);\n                                        border: 3px solid gray;\n                                        border-radius: 5px;\n                                        border-color: rgb(65,65,65);\n                                        color: white;\n                                        font-family: Microsoft YaHei UI;\n                                    }\n                                    QPushButton:pressed{\n                                        background-color: rgb(1,1,1);\n                                        border: 3px solid gray;\n                                        border-radius: 5px;\n                                        border-color: rgb(1,1,1);\n                                        color: white;\n                                        font-family: Microsoft YaHei UI;\n                                    }\n                                ')
            self.infer_error.addButton(
                confirm_button, QtWidgets.QMessageBox.YesRole)
            self.infer_error.setStyleSheet(
                '\n                                    QMessageBox {\n                                        font-family:Microsoft YaHei UI;\n                                        font-size:18px;\n                                        background-color:white;\n                                        border:5px solid gray;\n                                        border-radius:10px;\n                                    }\n                                ')
            self.infer_error.setWindowFlag(QtCore.Qt.FramelessWindowHint)
            self.infer_error.exec_()
        self.origin_img_path = ""

    def on_begin_button(self):
        img = cv2.imread(self.origin_img_path)
        mat = cv2.imread(self.mat_img_path)
        if self.origin_img_path=='' or self.mat_img_path == '':
            self.infer_error = QtWidgets.QMessageBox()
            self.infer_error.setWindowTitle('滤镜失败！')
            self.infer_error.setText(
                '请先上传原图并进行图像推理\n')
            confirm_button = QtWidgets.QPushButton('确定')
            confirm_button.setStyleSheet(
                '\n                                    QPushButton{\n                                        width: 60px;\n                                        height: 30px;\n                                        background-color: gray;\n                                        border: 3px solid gray;\n                                        border-radius: 5px;\n                                        color: white;\n                                        font-family: Microsoft YaHei UI;\n                                        font-size:20px;\n                                    }\n                                    QPushButton:hover{\n                                        background-color: rgb(65,65,65);\n                                        border: 3px solid gray;\n                                        border-radius: 5px;\n                                        border-color: rgb(65,65,65);\n                                        color: white;\n                                        font-family: Microsoft YaHei UI;\n                                    }\n                                    QPushButton:pressed{\n                                        background-color: rgb(1,1,1);\n                                        border: 3px solid gray;\n                                        border-radius: 5px;\n                                        border-color: rgb(1,1,1);\n                                        color: white;\n                                        font-family: Microsoft YaHei UI;\n                                    }\n                                ')
            self.infer_error.addButton(
                confirm_button, QtWidgets.QMessageBox.YesRole)
            self.infer_error.setStyleSheet(
                '\n                                    QMessageBox {\n                                        font-family:Microsoft YaHei UI;\n                                        font-size:18px;\n                                        background-color:white;\n                                        border:5px solid gray;\n                                        border-radius:10px;\n                                    }\n                                ')
            self.infer_error.setWindowFlag(QtCore.Qt.FramelessWindowHint)
            self.infer_error.exec_()
            return None
        # 黑白化
        # 背景
        # img 表示原图，mat表示抠图，front为True表示对前景进行变换
        # img=Blacken(img,mat,front=False)
        # 前景
        # img=Blacken(img,mat,front=True)
        # 反色
        # 背景
        # img=inverse_color(img,mat,front=False)
        # 前景
        # img=inverse_color(img,mat,front=False)
        # 虚化
        # 背景
        img = background_blur(img, mat, front=False)
        # 前景
        # img=background_blur(img,mat,front=True)
        cv2.imwrite("gui_utils/fillter/test.png", img)
        temp = QtGui.QPixmap("gui_utils/fillter/test.png")
        # temp = QtGui.QPixmap(self.origin_img_path)
        w, h = self.caculate_resize(temp.width(), temp.height())
        temp = temp.scaled(w, h)
        self.img_origin_label.setPixmap(temp)
        # file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
        #     self, '行选择要保存的路径', '', 'Image Files(*.png *.jpg *.bmp);;All Files (*)')
        # if file_path:
        #     if self.now_img == 'mask':
        #         a = cv2.imread(self.mask_img_path, cv2.IMREAD_UNCHANGED)
        #         cv2.imwrite(file_path, a)
        #     elif self.now_img == 'mat':
        #         a = cv2.imread(self.mat_img_path, cv2.IMREAD_UNCHANGED)
        #         cv2.imwrite(file_path, a)
        # else:
        #     print('save error')

    def on_import_factor_button(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, '请选择要推理的图片', '', 'Image Files(*.png *.jpg *.bmp);;All Files (*)')
        if file_name == '':
            return
        self.origin_img_path = file_name
        temp = QtGui.QPixmap(self.origin_img_path)
        w, h = self.caculate_resize(temp.width(), temp.height())
        temp = temp.scaled(w, h)
        self.img_origin_label.setPixmap(temp)
        self.begin.path = self.origin_img_path
        self.mask_img_path = ''
        self.mat_img_path = ''

    def on_export_sample_button(self):
        if self.origin_img_path:
            self.begin.run()
            self.mask_img_path = self.begin.mask_total_path
            self.mat_img_path = self.begin.mat_total_path
            self.infer_error = QtWidgets.QMessageBox()
            self.infer_error.setWindowTitle('推理成功！')
            self.infer_error.setText(
                '图像推理成功！本次推理用时：%.3fs   \n' % self.begin.time_run)
            confirm_button = QtWidgets.QPushButton('确定')
            confirm_button.setStyleSheet(
                '\n                                    QPushButton{\n                                        width: 60px;\n                                        height: 30px;\n                                        background-color: gray;\n                                        border: 3px solid gray;\n                                        border-radius: 5px;\n                                        color: white;\n                                        font-family: Microsoft YaHei UI;\n                                        font-size:20px;\n                                    }\n                                    QPushButton:hover{\n                                        background-color: rgb(65,65,65);\n                                        border: 3px solid gray;\n                                        border-radius: 5px;\n                                        border-color: rgb(65,65,65);\n                                        color: white;\n                                        font-family: Microsoft YaHei UI;\n                                    }\n                                    QPushButton:pressed{\n                                        background-color: rgb(1,1,1);\n                                        border: 3px solid gray;\n                                        border-radius: 5px;\n                                        border-color: rgb(1,1,1);\n                                        color: white;\n                                        font-family: Microsoft YaHei UI;\n                                    }\n                                ')
            self.infer_error.addButton(
                confirm_button, QtWidgets.QMessageBox.YesRole)
            self.infer_error.setStyleSheet(
                '\n                                    QMessageBox {\n                                        font-family:Microsoft YaHei UI;\n                                        font-size:18px;\n                                        background-color:white;\n                                        border:5px solid gray;\n                                        border-radius:10px;\n                                    }\n                                ')
            self.infer_error.setWindowFlag(QtCore.Qt.FramelessWindowHint)
            self.infer_error.exec_()
        else:
            self.infer_error = QtWidgets.QMessageBox()
            self.infer_error.setWindowTitle('错误')
            self.infer_error.setText('您还未选择任何图片！请点击左上角的选择图像按钮！')
            confirm_button = QtWidgets.QPushButton('确定')
            confirm_button.setStyleSheet(
                '\n                        QPushButton{\n                            width: 60px;\n                            height: 30px;\n                            background-color: gray;\n                            border: 3px solid gray;\n                            border-radius: 5px;\n                            color: white;\n                            font-family: Microsoft YaHei UI;\n                            font-size:20px;\n                        }\n                        QPushButton:hover{\n                            background-color: rgb(65,65,65);\n                            border: 3px solid gray;\n                            border-radius: 5px;\n                            border-color: rgb(65,65,65);\n                            color: white;\n                            font-family: Microsoft YaHei UI;\n                        }\n                        QPushButton:pressed{\n                            background-color: rgb(1,1,1);\n                            border: 3px solid gray;\n                            border-radius: 5px;\n                            border-color: rgb(1,1,1);\n                            color: white;\n                            font-family: Microsoft YaHei UI;\n                        }\n                    ')
            self.infer_error.addButton(
                confirm_button, QtWidgets.QMessageBox.YesRole)
            self.infer_error.setStyleSheet(
                '\n                        QMessageBox {\n                            font-family:Microsoft YaHei UI;\n                            font-size:18px;\n                            background-color:white;\n                            border:5px solid gray;\n                            border-radius:10px;\n                        }\n                    ')
            self.infer_error.setWindowFlag(QtCore.Qt.FramelessWindowHint)
            self.infer_error.exec_()

    def caculate_resize(self, w, h):
        if w > h:
            r = h / w
            iw = 1026
            ih = int(iw * r)
            if ih > 600:
                ih = 600
        else:
            r = w / h
            ih = 600
            iw = int(ih * r)
            if iw > 1026:
                iw = 1026
        return (
            iw, ih)

    def mousePressEvent(self, e):
        self.start_point = e.globalPos()
        self.window_point = self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        self.ismoving = True
        relpos = e.globalPos() - self.start_point
        self.move(self.window_point + relpos)

    def mouseReleaseEvent(self, e):
        self.ismoving = False


# 黑白化
def Blacken(img, mat, front=True):
    if front:
        mat = cv2.cvtColor(mat, cv2.COLOR_BGR2GRAY)
        mat = cv2.cvtColor(mat, cv2.COLOR_GRAY2BGR)
    else:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    img[mat != 0] = mat[mat != 0]
    return img


# 虚化
def background_blur(img, mat, front=True):
    if front:
        img_b = cv2.blur(img, (20, 20))
        mat_b = np.zeros_like(mat)
        mat_b[mat != 0] = img_b[mat != 0]
        mat = mat_b
    else:
        img = cv2.blur(img, (20, 20))
    img[mat != 0] = mat[mat != 0]
    return img


# 反色
def inverse_color(img, mat, front=True):
    if front:
        mat = 255 - mat
        img[mat != 255] = mat[mat != 255]
    else:
        img = 255 - img
        img[mat != 0] = mat[mat != 0]
    return img
