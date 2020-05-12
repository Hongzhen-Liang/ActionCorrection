import array
import serial
import threading
import numpy as np
import time
import pyqtgraph as pg

class sEMG_MYO():
    def __init__(self,portx,bps):
        '''sinscry肌电数据图像初始化'''
        self.sEMG_app = pg.mkQApp()  # 建立app
        self.sEMG_win = pg.GraphicsWindow()  # 建立窗口
        self.sEMG_win.setWindowTitle(u'pyqtgraph逐点画波形图')
        self.sEMG_win.resize(800, 500)  # 小窗口大小
        self.sEMG_data = array.array('d')  # 可动态改变数组的大小,double型数组
        self.sEMG_historyLength = 3000  # 横坐标长度
        self.sEMG_data=np.zeros(self.sEMG_historyLength).__array__('d')#把数组长度定下来
        self.sEMG_p = self.sEMG_win.addPlot()  # 把图p加入到窗口中
        self.sEMG_p.showGrid(x=True, y=True)  # 把X和Y的表格打开
        self.sEMG_p.setRange(xRange=[0, self.sEMG_historyLength], yRange=[0, 500], padding=0)
        self.sEMG_p.setLabel(axis='left', text='y / V')  # 靠左
        self.sEMG_p.setLabel(axis='bottom', text='x / point')
        self.sEMG_p.setTitle('semg')  # 表格的名字
        self.sEMG_curve = self.sEMG_p.plot()  # 绘制一个图形
        self.sEMG_curve.setData(self.sEMG_data)
        # portx = 'COM3'
        # bps = 115200
        # 串口执行到这已经打开 再用open命令会报错
        self.mSerial = serial.Serial(portx, int(bps))
        if (self.mSerial.isOpen()):
            print("open success")
            self.mSerial.write("hello".encode()) # 向端口些数据 字符串必须译码
            self.mSerial.flushInput()  # 清空缓冲区
        else:
            print("open failed")
            self.mSerial.close()  # 关闭端口
        self.sEMG_th1 = threading.Thread(target=self.Serial)#目标函数一定不能带（）被这个BUG搞了好久
        self.sEMG_th1.start()
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.plot_sEMG_Data)  # 定时刷新数据显示
        self.timer.start(0.000001)  # 多少ms调用一次
        self.sEMG_app.exec_()

    def Serial(self):
        i=0
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

    def plot_sEMG_Data(self):
        '''sinscry肌电图定时变化'''
        self.sEMG_p.setRange(yRange=[0, max(self.sEMG_data)])
        self.sEMG_curve.setData(self.sEMG_data)

if __name__=='__main__':
    EMG_MYO = sEMG_MYO("COM3",115200)