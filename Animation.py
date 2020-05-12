import array
import serial
import threading
import numpy as np
import time
import pyqtgraph as pg
import csv

i = 0
def Serial():
    csv_file = open('./Emg_data/幻椅式错误000.csv', 'w', newline='')
    csv_writer = csv.writer(csv_file)
    while(True):
        n = mSerial.inWaiting()
        if(n):
            if data!=" ":
                # dat = int.from_bytes(mSerial.readline(),byteorder='big')  # 格式转换
                dat = mSerial.readline()
                dat = dat.decode()
                dat = dat.split('\r')[0]
                # print(dat)
                while dat=='' or dat=='\n':
                    dat = mSerial.readline()
                    dat = dat.decode()
                    dat = dat.split('\r')[0]
                dat = int(dat)
                csv_writer.writerow([dat])
                n=0
                global i
                if i < historyLength:
                    data[i] = dat
                    i = i+1
                else:
                    data[:-1] = data[1:]
                    data[i-1] = dat
        # Max_data=max(data)

    csv_file.close()

def plotData():
    p.setRange(yRange=[0, max(data)]    )
    curve.setData(data)
    # Sum = 0
    # S_or_E = 0
    # for i in range(historyLength//10):
    #     Sum += data[i]
    # if Sum > 20:
    #     print('start')
    #     S_or_E = 1
    # elif S_or_E==1 and Sum < 5:
    #     print('end')



if __name__ == "__main__":
    app = pg.mkQApp()  # 建立app
    win = pg.GraphicsWindow()  # 建立窗口
    win.setWindowTitle(u'pyqtgraph逐点画波形图')
    win.resize(800, 500)  # 小窗口大小
    data = array.array('d')  # 可动态改变数组的大小,double型数组
    historyLength = 500  # 横坐标长度
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
    portx = 'COM4'
    bps = 115200
    # 串口执行到这已经打开 再用open命令会报错
    mSerial = serial.Serial(portx, int(bps))
    if (mSerial.isOpen()):
        print("open success")
        mSerial.write("hello".encode()) # 向端口些数据 字符串必须译码
        mSerial.flushInput()  # 清空缓冲区
    else:
        print("open failed")
        serial.close()  # 关闭端口
    th1 = threading.Thread(target=Serial)#目标函数一定不能带（）被这个BUG搞了好久
    th1.start()
    timer = pg.QtCore.QTimer()
    timer.timeout.connect(plotData)  # 定时刷新数据显示
    timer.start(0.000001)  # 多少ms调用一次
    app.exec_()
