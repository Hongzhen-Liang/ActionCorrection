import array
import serial
import threading
import numpy as np
import time
import pyqtgraph as pg
import csv
from sinscry_fun import mean
from pandas.core.frame import DataFrame
import numpy as np
import pandas as pd
from scipy.fftpack import fft,ifft

def Serial():
    i=0
    sta = True
    end = False
    jump_value=0
    thre = 5
    tmp = []
    React = 0
    while(True):
        Y_N = mSerial.inWaiting()
        if Y_N:
            # dat = int.from_bytes(mSerial.readline(),byteorder='big')  # 格式转换
            dat = mSerial.readline()
            dat = dat.decode("utf8","ignore")
            dat = dat.split('\r')[0]
            while dat=='' or dat=='\n':
                dat = mSerial.readline()
                dat = dat.decode("utf8","ignore")
                dat = dat.split('\r')[0]
            dat = int(dat)
            # print(dat)
            if i < historyLength:
                data[i] = dat
                i +=1
            else:
                data[:-1] = data[1:]
                data[i-1] = dat

                if not React:
                    jump_value+=1
                    if jump_value<100:
                        continue
                    jump_value=0

                if React:
                    tmp.append(dat)
                elif sta and mean(data)>thre:
                    print('起')
                    React=1
                    sta = False
                    end = True
                
                if end and mean(data)<thre:
                    print('落')
                    React=0
                    sta=True
                    end=False
                    
                    if len(tmp)<1000:
                        print('时间太短')
                    else:
                        mav_action=pd.DataFrame(columns=['ch1_mean','ch1_pow_mean','ch1_len','ch1_fft_mean'])
                        mav_action.loc[0,'ch1_mean']=mean(tmp)
                        mav_action.loc[0,'ch1_pow_mean']=np.sum(np.array(tmp)**2)/len(tmp)
                        mav_action.loc[0,'ch1_len']=len(tmp)
                        mav_action.loc[0,'ch1_fft_mean']=mean(abs(fft(tmp)))
                        
                        # model = joblib.load("train_model.m")  # 提取模型
                        # print('pred =', model.predict(mav_action))     
                    tmp=[]

                    


def plotData():
    p.setRange(yRange=[0, max(data)])
    curve.setData(data)

if __name__ == "__main__":
    app = pg.mkQApp()  # 建立app
    win = pg.GraphicsWindow()  # 建立窗口
    win.setWindowTitle(u'pyqtgraph逐点画波形图')
    win.resize(800, 500)  # 小窗口大小
    data = array.array('d')  # 可动态改变数组的大小,double型数组
    historyLength = 3000  # 横坐标长度
    a = 0
    data=np.zeros(historyLength).__array__('d')#把数组长度定下来
    p = win.addPlot()  # 把图p加入到窗口中
    p.showGrid(x=True, y=True)  # 把X和Y的表格打开
    p.setRange(xRange=[0, historyLength], yRange=[0, 500], padding=0)
    p.setLabel(axis='left', text='y / V')  # 靠左
    p.setLabel(axis='bottom', text='x / point')
    p.setTitle('semg')  # 表格的名字
    curve = p.plot()  # 绘制一个图形
    curve.setData(data)
    portx = 'COM3'
    bps = 115200
    # 串口执行到这已经打开 再用open命令会报错
    mSerial = serial.Serial(portx, int(bps))
    if (mSerial.isOpen()):
        print("open success")
        mSerial.write("hello".encode()) # 向端口些数据 字符串必须译码
        mSerial.flushInput()  # 清空缓冲区
    else:
        print("open failed")
        mSerial.close()  # 关闭端口
    th1 = threading.Thread(target=Serial)#目标函数一定不能带（）被这个BUG搞了好久
    th1.start()
    timer = pg.QtCore.QTimer()
    timer.timeout.connect(plotData)  # 定时刷新数据显示
    timer.start(0.001)  # 多少ms调用一次
    app.exec_()
