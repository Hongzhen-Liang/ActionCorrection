import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame
import csv
import joblib
# get_move_window:移动窗口图,cut_sta_end:找出起止点
from sinscry_fun import plot_photo,get_move_window,mean,cut_sta_end,sEmg_train




# 初始设置
windowlength = 3000
thre = 2
Right=[]
Lower=[]
Uper=[]
# 读取数据
for i in range(3):
    Right.append(pd.read_csv('./平板支撑/平板正确00'+str(i)+'.csv'))
    Lower.append(pd.read_csv('./平板支撑/平板低臀00'+str(i)+'.csv'))
    Uper.append(pd.read_csv('./平板支撑/平板提臀00'+str(i)+'.csv'))
    Right[i].columns = ['ch1']
    Lower[i].columns = ['ch1']
    Uper[i].columns = ['ch1']
for i in range(3,5):
    Right.append(pd.read_csv('./平板支撑/平板正确00'+str(i)+'.csv'))
    Right[i].columns = ['ch1']
plot_photo(Right[0],'Plank')
plot_photo(get_move_window(Right[0],windowlength),'Plank_movewindow')
# plot_photo(Lower[0],'Plank_Lower','maroon')
# plot_photo(get_move_window(Lower[0],windowlength),'Plank_Lower_movewindow','maroon')
# plot_photo(Uper[0],'Plank_Uper','darkcyan')
# plot_photo(get_move_window(Uper[0],windowlength),'Plank_Uper_movewindow','darkcyan')
# plt.show()
# 开始设置训练动作
mav_Right = pd.DataFrame(columns=['ch1_mean','ch1_pow_mean','ch1_len','ch1_fft_mean'])
mav_Lower = pd.DataFrame(columns=['ch1_mean','ch1_pow_mean','ch1_len','ch1_fft_mean'])
mav_Uper = pd.DataFrame(columns=['ch1_mean','ch1_pow_mean','ch1_len','ch1_fft_mean'])
sEmg_train(mav_Right,Right,thre,windowlength) # 训练函数
sEmg_train(mav_Lower,Lower,thre,windowlength)
sEmg_train(mav_Uper,Uper,thre,windowlength)

mav_Right['action']='平板支撑:身体成一条直线,动作正确'
mav_Lower['action']='平板支撑:向下塌腰,动作错误'
mav_Uper['action']='平板支撑:向上拱臀，动作错误'
sumup = mav_Right.append([mav_Lower, mav_Uper], ignore_index=True)
y = sumup.action
x = sumup.drop(['action'],axis=1)

'''机器学习'''
from sklearn.model_selection import train_test_split
from sklearn import svm
train_x,test_x,train_y,test_y = train_test_split(x, y, test_size=0.2)
model = svm.SVC(kernel='linear', C=0.8)
model.fit(train_x,train_y)
print(model.score(train_x,train_y))
joblib.dump(model, "Plank.m")  # 保存模型
print('pred =', model.predict(x))

