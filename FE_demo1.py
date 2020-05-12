import json
import sys
import threading

import cv2
import joblib
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5.QtWidgets import *

# sinscry的代码----------------------
import csv
import time
import array
import serial
import Select_win
import Sign_In
import Sign_Up
import pyqtgraph as pg
from sql_execute import sql_insert,sql_login,sql_integral,MD5 # sinscry自定义
from sinscry_fun import sEMG_MYO
import joblib
from FE_traing import Ui_MainWindow
import getKeyPoint_fromPic
import judgeAction


class ui(Ui_MainWindow, QMainWindow):
    cap = None  # 摄像机流
    train_img = None  # 摄像机帧的数组
    key_point = None  # 关键点
    key_point_color = None  # 关键点颜色

    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)

        self.key_point_color = [(0, 0, 255)] * 22  # 身体关键点颜色

        # 播放训练视频
        self.player = QMediaPlayer(self)
        self.player.setVideoOutput(self.videoWidget)  # 视频播放输出的widget，就是上面定义的
        self.timer_train = QTimer()  # 初始化训练进度定时器，控制标准动作集json的跳转
        self.timer_train.timeout.connect(lambda: threading.Thread(target=self.jdg_standard).start())  # 若定时器结束，从视频流中抓取一帧去识别动作标准程度

        # 默认打开摄像头，并显示到小窗口处
        self.if_open_camera = 0  # 1为现在是打开摄像头的状态，0是不打开摄像头的状态
        self.open_camera.clicked.connect(self.openCamera)
        self.close_camera.clicked.connect(self.closeCamera)
        self.timer_camera = QTimer()  # 初始化定时器，用户控制显示视频的帧率
        self.timer_camera.timeout.connect(self.showCamera)  # 若定时器结束，则调用show_camera()

        # 拍全身照
        self.timer_whole_pic = QTimer()
        self.count = 5  # 倒计时，取5次的平均值为标准身材数据
        self.standard_key_point = [[[0.0, 0.0] for j in range(2)] for k in range(22)]
        self.timer_whole_pic.timeout.connect(self.take_whole_body_pic)

        # 创建一个关闭事件并设为未触发
        self.stopEvent = threading.Event()
        self.stopEvent.clear()

        # 控制视频（训练）开始/暂停【一开始隐藏按钮】
        self.if_training = 0  # 1：训练ing; 0：并没有训练
        self.btn_more.clicked.connect(self.more)  # more, 点击显示“开始训练|暂停训练|结束训练”
        self.btn_startTraining.clicked.connect(self.startTraining)  # play
        self.btn_stopTraining.clicked.connect(self.pauseTraining)  # pause
        self.pushButton.clicked.connect(self.endTrain)

        # 初始化页面显示
        self.open_camera.setHidden(True)
        self.close_camera.setHidden(True)
        self.btn_startTraining.setHidden(True)
        self.btn_stopTraining.setHidden(True)

        # 进训练页面，先选取教学视频（为下一步在另一个窗口先选中视频再跳转该页面直接开始训练做铺垫）
        # self.player.setMedia(QMediaContent(QFileDialog.getOpenFileUrl()[0]))  # 手动选择视频文件
        # self.openCamera()  # 默认自动打开摄像头

        # 显示动作提示内容
        self.actions_tips = '先来做一组5秒的平板支撑作为热身活动吧！请与教学视频的动作保持一致'
        self.tips_label.setText(self.actions_tips)

        # 自动跳转标准数据集
        self.change_standard_data_timer = QTimer()
        self.change_standard_data_timer.timeout.connect(self.change_standard_data)
        self.data_list_name = []
        self.start_time = []
        self.end_time = []
        self.index = 0
        self.length_standard_data = 0  # 数据集的数量
        self.standard_data = {}
        self.open_standard_data()
        self.EMG_MYO = None
        self.have_sEMG_photo = 0
        try:
            self.EMG_MYO = sEMG_MYO('COM3',115200)
            self.sEMG_tips_label.setText('检测到肌电装置')
        except:
            self.sEMG_tips_label.setText('提示:未检测到肌电装置')

    def more(self):
        # self.btn_more.setHidden(True)  # 先不隐藏它，后面优化交互再说
        if self.if_open_camera == 1:
            self.close_camera.setHidden(False)
            self.open_camera.setHidden(True)
        elif self.if_open_camera == 0:
            self.open_camera.setHidden(False)
            self.close_camera.setHidden(True)
        if self.if_training == 1:
            self.btn_stopTraining.setHidden(False)
            self.btn_startTraining.setHidden(True)
        elif self.if_training == 0:
            self.btn_startTraining.setHidden(False)
            self.btn_stopTraining.setHidden(True)
    
    def endTrain(self):
        sys.exit(0)

    def startTraining(self):
        """
            点击播放键执行开始训练函数
            :return:
            """
        if self.cap is None:
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 初始化摄像头
        self.timer_camera.start(0)
        self.player.setMedia(QMediaContent(QUrl("./videos/fcoach.mp4")))

        self.count = 5
        self.timer_whole_pic.start(2000)
        self.if_training = 1
        self.timer_train.start(1000)  # 开始训练计时

        '''开始肌电数据获取,EMG_MYO是肌电数据类'''
        # try:
        if self.have_sEMG_photo==0:
            if not self.EMG_MYO:
                QtWidgets.QMessageBox.critical(video_gui, "错误", "未安装肌电装置")
            else:
                self.EMG_MYO.Sta(self.sEMG_tips_label)
            self.have_sEMG_photo=1

    def pauseTraining(self):
        self.if_training = 0
        self.player.pause()
        self.timer_train.stop()  # 暂停训练计时
        print(int(self.player.position() / 1000))

    def openCamera(self):
        self.if_open_camera = 1
        if self.cap is None:
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.timer_camera.isActive():  # 若定时器未启动
            flag = self.cap.open(0)
            if not flag:  # 如果open不成功
                msg = QMessageBox.warning(self, 'warning', "请检查相机于电脑是否连接正确", buttons=QMessageBox.Ok)
            else:
                self.timer_camera.start(10)  # 定时器开始计时10ms，结果是每过30ms从摄像头取一帧显示

        # th = threading.Thread(target=self.show_camera)
        # th.start()

    def closeCamera(self):
        self.if_open_camera = 0
        self.timer_camera.stop()  # 关闭定时器
        self.cap.release()  # 释放视频流
        self.cameraLabel.clear()  # 清空视频显示区域

    def showCamera(self):
        flag, show = self.cap.read()  # 从视频流中读取
        if not flag:  # 如果这帧读取失败了，就返回
            return
        show = cv2.resize(show, (640, 480))  # 把读到的帧的大小重新设置为 640x480
        show = cv2.flip(show, 1)  # 水平翻转
        self.train_img = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        getKeyPoint_fromPic.draw_human(self.train_img, self.key_point, self.key_point_color)
        show_img = QImage(self.train_img.data, self.train_img.shape[1], self.train_img.shape[0],
                          QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        self.cameraLabel.setPixmap(QPixmap.fromImage(show_img))  # 往显示视频的Label里 显示QImage
        self.tips_label.setText(self.actions_tips)  # 显示动作的提示文字

    # TODO: 控制 检测动作完成度
    def control_judgement(self):
        if not self.timer_train.isActive():  # 若定时器未启动
            flag = self.if_training
            if not flag:  # 如果教练视频没有成功播放
                QMessageBox.warning(self, 'warning', '请检查教学视频是否存在', buttons=QMessageBox.Ok)
            else:
                self.timer_train.start(1000)  # 定时器开始计时1s，每1s从摄像头取一帧用来检测
                self.jdg_standard()

    def jdg_standard(self):
        try:
            self.key_point = getKeyPoint_fromPic.getkp_fpicture(self.key_point, self.train_img)
            if self.key_point:
                print("开始识别")
                self.actions_tips = judgeAction.jdg_if_correct(self.standard_data, self.key_point, self.key_point_color)
        except KeyError:
            print("识别到没人")
            pass

    # TODO： 获取用户标准的身体骨架信息
    def take_whole_body_pic(self):
        if self.count == 5:  # 首次进入，提示
            print("先来做一组5秒的平板支撑作为热身活动吧！请与教学视频的动作保持一致。")
            print("~~~请将摄像头放在与您热身时身体水平的高度~~~")
            pass
        getKeyPoint_fromPic.getkp_fpicture(self.key_point, self.train_img)
        try:
            self.standard_key_point = list((np.array(self.standard_key_point) + np.array(self.key_point)) / 2)
        except ValueError:
            pass
        except TypeError:
            pass
        self.count -= 1
        if self.count <= 0:  # 拍完照后，开始训练
            self.timer_whole_pic.stop()
            self.control_judgement()
            # media_file = QFileDialog.getOpenFileUrl()[0]
            # self.player.setMedia(QMediaContent(media_file))  # 手动选择视频文件
            getKeyPoint_fromPic.write_standard_data2json(self.standard_key_point, 'Standard')
            self.change_standard_data_timer.start(0)
            self.player.play()

    # TODO：打开动作训练List，获得每个训练集的名字、开始时间和结束时间
    def open_standard_data(self):
        with open('Data/List.json', 'r')as f:
            data_list = json.load(f)
            for keys in data_list.keys():
                self.data_list_name.append(keys)
                self.start_time.append(data_list[keys][0])
                self.end_time.append(data_list[keys][1])
                self.length_standard_data += 1

    def change_standard_data(self):
        print("-------------------------------------------------------------------------现在！！！打开了————index" + str(
            self.index) + ':' + str(
            self.data_list_name[self.index]) + "文件啦！！！！----------------------------------------")
        with open('Data/' + self.data_list_name[self.index] + '.json', 'r')as f1:
            self.standard_data = json.load(f1)
            if self.EMG_MYO:
                print('yes.m!!!!!!!!!!!!!!')
                model = joblib.load('Data/'+str(self.data_list_name[self.index])+'.m')  # 提取模型
                self.EMG_MYO.model.append(model)

        '''sinscry猫伸展不做判断'''
        if self.EMG_MYO:
            self.EMG_MYO.model_index = self.index

        self.index += 1
        self.change_standard_data_timer.stop()
        if self.length_standard_data == self.index:
            return
        t = self.start_time[self.index] - self.start_time[self.index - 1]
        self.change_standard_data_timer.start(t * 1000)


# Ui跳转:从f界面跳转到t界面
def jump_to(f, t):
    t.show()
    f.close()


# 注册函数
def sign_up():
    id_up = ui_up.btn_id.text()
    psw_up = ui_up.btn_psw.text()
    psw_up_reply = ui_up.btn_psw1.text()
    if psw_up != psw_up_reply:
        QtWidgets.QMessageBox.critical(SignUp, "错误", "两次输入密码不相同")
    else:
        if sql_insert(id_up, MD5(psw_up)):
            QtWidgets.QMessageBox.critical(SignUp, "错误", "用户已注册")
        else:
            QtWidgets.QMessageBox.about(SignUp, "成功", "注册成功")
            jump_to(SignUp, Login)


# 登录函数
def sign_in():
    id_in = ui_in.login_username.text()
    psw_in = ui_in.login_psw.text()
    status, psw_in_sql = sql_login(id_in)
    if not status:
        QtWidgets.QMessageBox.critical(Login, "错误", "用户未注册")
    elif psw_in_sql == MD5(psw_in):  # 注册成功时
        integral_in = sql_integral(id_in)  # 查询积分函数
        ui_select.btn_integral.setText(str(integral_in))
        ui_select.id_label.setText(id_in)
        jump_to(Login, Select)
    else:
        QtWidgets.QMessageBox.critical(Login, "错误", "密码错误")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 登入界面
    Login = QMainWindow()
    ui_in = Sign_In.Ui_Dialog()
    ui_in.setupUi(Login)
    Login.show()

    # 注册界面
    SignUp = QMainWindow()
    ui_up = Sign_Up.Ui_Dialog()
    ui_up.setupUi(SignUp)

    # 选择界面
    Select = QMainWindow()
    ui_select = Select_win.Ui_MainWindow()
    ui_select.setupUi(Select)

    # 训练界面
    video_gui = ui()

    # 跳转界面(Login:登录界面,SignUp:注册界面,Select:选择课程界面,video_gui:训练界面)
    ui_in.btn_register.clicked.connect(lambda: jump_to(Login, SignUp))  # 从登录界面跳到注册界面
    ui_in.btn_login.clicked.connect(sign_in)  # 登录函数操作 + mysql数据库操作
    ui_up.btn_register.clicked.connect(sign_up)  # 注册函数操作+mysql数据库操作
    ui_select.btn_start.clicked.connect(lambda: jump_to(Select, video_gui))  # 从选择界面跳到训练界面
    ui_select.btn_logout.clicked.connect(lambda: jump_to(Select, Login))  # 从选择界面返回登录界面

    # video_gui.show()

    # VideoToPicture.pre_process(self.key_point, self.lineup)  # 预处理，拍全身照，得到标准骨架信息

    sys.exit(app.exec_())
