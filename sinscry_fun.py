import array
import serial
import threading
import time
import pyqtgraph as pg
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame
import numpy as np
from scipy.fftpack import fft,ifft
import pandas as pd
import joblib
import multiprocessing




# 绘图函数
def plot_photo(data,title,c='steelblue'):
    plt.figure()
    plt.plot(data,c=c)
    plt.title(title)
    # plt.show()

# 移动窗口函数
def get_move_window(mean_semg,windowlength):
    mean_semg_arr = DataFrame(mean_semg)
    mean_semg_arr = mean_semg_arr.rolling(windowlength).mean()
    mean_semg_arr = np.array(mean_semg_arr)
    return mean_semg_arr

# 求平均数函数
def mean(data):
    sum = 0
    len_data=len(data)
    for i in range(len_data):
        sum+=data[i]
    return sum/len_data

# 求起止点函数
def cut_sta_end(data,thre,windowlength):
    data=data.values
    move_win = []
    for j in range(windowlength):
        move_win.append(data[j][0])
    sta = True
    end = False
    sta_num = end_num = jump_value = 0
    for j in range(windowlength,len(data)):
        move_win[:-1]=move_win[1:]
        move_win[windowlength-1]=data[j][0]
        
        # 每隔100才做一次计算
        jump_value+=1
        if jump_value<100:
            continue
        jump_value=0
        
        if sta and mean(move_win)>thre:
            # print('起',j)
            sta_num  = j
            sta = False
            end = True
        elif end and mean(move_win)<thre:
            # print('落',j)
            end_num = j
            sta = True
            end = False
            if end_num-sta_num<2500:
                print('持续时间不够')
            else:
                break
    return sta_num,end_num

def sEmg_train(mav_action,Action,thre,windowlength):
    for i in range(len(Action)):
        sta,end=cut_sta_end(Action[i],thre,windowlength)
        tmp = Action[i][sta:end]
        # print(tmp)
        print(sta,end)
        mav_action.loc[i,'ch1_mean']=tmp.ch1.mean()
        mav_action.loc[i,'ch1_pow_mean']=((tmp.ch1)**2).mean()
        mav_action.loc[i,'ch1_len']=end-sta
        data_cut1 = []
        for j in range(len(tmp)):
            data_cut1.append(tmp.values[j][0])
        # plot_photo(data_cut1,'fft')
        yy = abs(fft(data_cut1))
        mav_action.loc[i,'ch1_fft_mean']=mean(yy)



def sEMG_photo(mul_EMG_data):
    def plot_sEMG_Data():
        sEMG_data=[]
        for i in range(len(mul_EMG_data)):
            sEMG_data.append(mul_EMG_data[i])
        '''sinscry肌电图定时变化'''
        sEMG_p.setRange(yRange=[0, max(sEMG_data)])
        sEMG_curve.setData(sEMG_data)
    sEMG_data=[]
    for i in range(len(mul_EMG_data)):
        sEMG_data.append(mul_EMG_data[i])
    '''sinscry肌电数据图像初始化'''
    sEMG_historyLength=3000
    sEMG_app = pg.mkQApp()  # 建立app
    sEMG_win = pg.GraphicsWindow()  # 建立窗口
    sEMG_win.setWindowTitle(u'pyqtgraph逐点画波形图')
    sEMG_win.resize(800, 500)  # 小窗口大小
    sEMG_p = sEMG_win.addPlot()  # 把图p加入到窗口中
    sEMG_p.showGrid(x=True, y=True)  # 把X和Y的表格打开
    sEMG_p.setRange(xRange=[0, sEMG_historyLength], yRange=[0, 500], padding=0)
    sEMG_p.setLabel(axis='left', text='y / V')  # 靠左
    sEMG_p.setLabel(axis='bottom', text='x / point')
    sEMG_p.setTitle('semg')  # 表格的名字
    sEMG_curve = sEMG_p.plot()  # 绘制一个图形
    sEMG_curve.setData(sEMG_data)
    timer = pg.QtCore.QTimer()
    timer.timeout.connect(plot_sEMG_Data)  # 定时刷新数据显示
    timer.start(0.000001)  # 多少ms调用一次
    sEMG_app.exec_()







class sEMG_MYO():
    def __init__(self,portx,bps):
        self.mSerial = serial.Serial(portx, int(bps))
        self.model=[]
        self.model_index=-1
        self.sEMG_thre=[2,2,15,15,10]
        self.sEMG_historyLength = 3000  # 横坐标长度
        self.sEMG_data = array.array('d')  # 可动态改变数组的大小,double型数组
        self.sEMG_data=np.zeros(self.sEMG_historyLength).__array__('d')#把数组长度定下来
        self.sEMG_data=multiprocessing.Array("d",self.sEMG_data)
        


    def Sta(self,sEMG_tips_label=None):
        self.sEMG_tips_label = sEMG_tips_label
        # self.mSerial = serial.Serial(portx, int(bps))
        if self.mSerial.isOpen():
            print("open success")
            self.mSerial.write("hello".encode()) # 向端口些数据 字符串必须译码
            self.mSerial.flushInput()  # 清空缓冲区
        else:
            print("open failed")
            self.mSerial.close()  # 关闭端口
        self.sEMG_th1 = threading.Thread(target=self.Serial)#目标函数一定不能带（）被这个BUG搞了好久
        self.sEMG_th1.start()
        p=multiprocessing.Process(target=sEMG_photo,args=(self.sEMG_data,))
        p.start()

    # def plot_sEMG_Data(self):
    #     '''sinscry肌电图定时变化'''
    #     self.sEMG_p.setRange(yRange=[0, max(self.sEMG_data)])
    #     self.sEMG_curve.setData(self.sEMG_data)


    def Serial(self):
        if self.sEMG_tips_label:
            self.sEMG_tips_label.setText('肌电开始运作')
        sta=True
        end=False
        i=0
        jump_value=0
        React=0
        tmp=[]
        while(True):
            n = self.mSerial.inWaiting()
            if(n):
                if self.sEMG_data!=" ":
                    # dat = int.from_bytes(mSerial.readline(),byteorder='big')  # 格式转换
                    dat = self.mSerial.readline()
                    try:
                        dat = dat.decode()
                    except:
                        print("decode()失败"+str(dat))
                        continue
                    dat = dat.split('\r')[0]
                    # print(dat)
                    while dat=='' or dat=='\n':
                        dat = self.mSerial.readline()
                        dat = dat.decode()
                        dat = dat.split('\r')[0]
                    try:
                        dat = int(dat)
                    except:
                        print('int()失败'+str(dat))
                        continue
                    if i < self.sEMG_historyLength:
                        self.sEMG_data[i] = dat
                        i = i+1
                    else:
                        self.sEMG_data[:-1] = self.sEMG_data[1:]
                        self.sEMG_data[i-1] = dat
                        
                        if not React:
                            jump_value+=1
                            if jump_value<100:
                                continue
                            jump_value=0
                        
                        if self.model_index!=-1:
                            # 非猫伸展外动作进行svm判断
                            if React:
                                tmp.append(dat)
                            elif sta and mean(self.sEMG_data)>self.sEMG_thre[self.model_index]:
                                print('起')
                                if self.sEMG_tips_label:
                                    self.sEMG_tips_label.setText('肌电装置检测到动作开始')
                                React=1
                                sta=False
                                end=True
                            
                            if React:
                                jump_value+=1
                                if jump_value<100:
                                    continue
                                jump_value=0
                            
                            if end and mean(self.sEMG_data)<self.sEMG_thre[self.model_index]:
                                print('落')
                                if self.sEMG_tips_label:
                                    self.sEMG_tips_label.setText('肌电装置检测到动作结束')
                                React=0
                                sta=True
                                end=False
                                if len(tmp)<2500:
                                    print('持续时间不够')
                                    if self.sEMG_tips_label:
                                        self.sEMG_tips_label.setText('肌电装置检测到动作持续时间不足')
                                elif self.model_index!=0:
                                    mav_action=pd.DataFrame(columns=['ch1_mean','ch1_pow_mean','ch1_len','ch1_fft_mean'])
                                    mav_action.loc[0,'ch1_mean']=mean(tmp)
                                    mav_action.loc[0,'ch1_pow_mean']=np.sum(np.array(tmp)**2)/len(tmp)
                                    mav_action.loc[0,'ch1_len']=len(tmp)
                                    mav_action.loc[0,'ch1_fft_mean']=mean(abs(fft(tmp)))
                                    # model = joblib.load("train_model.m")  # 提取模型
                                    tmp_model = self.model[self.model_index]
                                    print('pred =', tmp_model.predict(mav_action))
                                    if self.sEMG_tips_label:
                                        self.sEMG_tips_label.setText(str(tmp_model.predict(mav_action)))
                                tmp=[]
                            







if __name__=='__main__':
    data_list_name=['CatStretch','Plank','Chair','RightMagicChairTwist','RightTriangleStretch']
    EMG_MYO = sEMG_MYO("COM3",115200)
    EMG_MYO.Sta()
    EMG_MYO.model_index=1
    for i in range(EMG_MYO.model_index+1):
        model = joblib.load('Data/'+str(data_list_name[i])+'.m')  # 提取模型
        EMG_MYO.model.append(model)
    print('yes')
    # model = joblib.load('Data/Plank.m')



