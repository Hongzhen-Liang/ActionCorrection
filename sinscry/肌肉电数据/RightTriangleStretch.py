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
thre = 10
Right=[]
Wrong=[]
Wrong_back=[]
# 读取数据
for i in range(3):
    Right.append(pd.read_csv('./右侧三角伸展式/三角00'+str(i)+'.csv'))
    Wrong.append(pd.read_csv('./右侧三角伸展式/三角错00'+str(i)+'.csv'))
    Wrong_back.append(pd.read_csv('./右侧三角伸展式/三角后错00'+str(i)+'.csv'))
    Right[i].columns = ['ch1']
    Wrong[i].columns = ['ch1']
    Wrong_back[i].columns = ['ch1']
plot_photo(Right[0],'RightTriangleStretetch')
plot_photo(get_move_window(Right[2],windowlength),'RightTriangleStretetch_move')
plot_photo(Wrong[0],'RightTriangleStretetch_Wrong','maroon')
plot_photo(get_move_window(Wrong[0],windowlength),'RightTriangleStretetch_Wrong_move','maroon')
plot_photo(Wrong_back[0],'RightTriangleStretetch_WrongBack','darkcyan')
plot_photo(get_move_window(Wrong_back[0],windowlength),'RightTriangleStretetch_WrongBack_move','darkcyan')
plt.show()

# 开始设置训练动作
mav_Right = pd.DataFrame(columns=['ch1_mean','ch1_pow_mean','ch1_len','ch1_fft_mean'])
mav_Wrong = pd.DataFrame(columns=['ch1_mean','ch1_pow_mean','ch1_len','ch1_fft_mean'])
mav_Wrong_back = pd.DataFrame(columns=['ch1_mean','ch1_pow_mean','ch1_len','ch1_fft_mean'])
sEmg_train(mav_Right,Right,thre,windowlength) # 训练函数
sEmg_train(mav_Wrong,Wrong,thre,windowlength)
sEmg_train(mav_Wrong_back,Wrong_back,thre,windowlength)

mav_Right['action']='右侧三角伸展式:胯部平行向左移,动作正确'
mav_Wrong['action']='右侧三角伸展式:胯部稍微向前扭转,动作不规范'
mav_Wrong_back['action']='右侧三角伸展式:胯部稍微向后扭转,动作不规范'
sumup = mav_Right.append([mav_Wrong, mav_Wrong_back], ignore_index=True)
y = sumup.action
x = sumup.drop(['action'],axis=1)

'''机器学习'''
from sklearn.model_selection import train_test_split
from sklearn import svm
train_x,test_x,train_y,test_y = train_test_split(x, y, test_size=0.2)
model = svm.SVC(kernel='linear', C=0.8)
model.fit(train_x,train_y)
print(model.score(train_x,train_y))
joblib.dump(model, "RightTriangleStretch.m")  # 保存模型

