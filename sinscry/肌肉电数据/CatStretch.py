import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame
import csv
# from sklearn.externals import joblib
import joblib
import threading
from sinscry_fun import plot_photo,get_move_window,mean

windowlength = 3000
thre = 2


if __name__ == "__main__":
    # 读取数据
    data1 = pd.read_csv('./猫伸展/猫000.csv')
    plot_photo(data1,'CatStretch')
    # 移动窗口图
    plot_photo(get_move_window(data1,windowlength),'CatStretch_movewindow')
    # plt.show()

    data = data1.values # pandas转array

    move_win = []
    for j in range(windowlength):
        move_win.append(data[j][0])

    sta = True
    end = False
    sta_num = end_num = 0
    count = 0   # 记载数组
    for i in range(windowlength,len(data)):
        if sta and mean(move_win)>thre:
            print('起',i)
            sta_num = i
            sta=False
            end=True
        elif end and mean(move_win)<thre:
            print('落',i)
            end_num = i
            sta=True
            end=False
            if end_num-sta_num>2500:
                count+=1
                print('---')
            else:
                print('持续时间不够')
        move_win[:-1]=move_win[1:]
        move_win[windowlength-1]=data[i][0]
    print('运动组数',count)



