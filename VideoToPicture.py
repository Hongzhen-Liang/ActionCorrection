import os
import cv2
import json
import getKeyPoint_fromPic
import judgeAction
import time

import array
# import serial
import threading
import numpy as np
# import pyqtgraph as pg
import csv

from Animation import Serial

'''
sinscry
多线程获取数据
'''
def EMG_Serial():
    mSerial = serial.Serial('COM3', 115200)  # 打开串口
    i = 0
    while(True):
        n = mSerial.inWaiting()
        if(n):
            if EMG_data!=" ":
                dat = mSerial.readline()
                dat = dat.decode()
                dat = dat.split('\r')[0]
                # print(dat)
                while dat=='' or dat =='\n':
                    dat = mSerial.readline()
                    dat = dat.decode()
                    dat = dat.split('\r')[0]
                dat = int(dat)
                n = 0
                if i < historyLength:
                    EMG_data[i] = dat
                    i += 1
                else:
                    EMG_data[:-1] = EMG_data[1:]
                    EMG_data[i-1] = dat

def EMG_determine():
    Sum = 0
    startN = 20  # 开始的和
    endN = 5    # 结束的和
    for i in range(historyLength/10):
        Sum += EMG_data[i]
    if Sum > startN:
        # print('start')
        S_or_E = 1
        return 1
    # FIXME: 这一段写的有问题，S_or_E没定义
    elif S_or_E==1 and Sum<endN:
        # print('end')
        S_or_E = 0
        return 0


def pre_process(key_point, lineup):
    # TODO：拍摄/获取用户全身照and预处理
    # 实际应用中，需要持续捕捉用户全身照，直到符合标准为止
    whole_body_pic_name = 'whole_body'
    pic_file_location = './img_input/' + whole_body_pic_name + '.jpg'
    whole_body_pic = cv2.imread(pic_file_location)

    getKeyPoint_fromPic.getkp_fpicture(key_point, whole_body_pic)

    print(whole_body_pic_name)
    skeleton_length = getKeyPoint_fromPic.cal_skeleton_length(lineup, key_point, whole_body_pic)  # 骨架长度

    # TODO: 将该训练的所有需要新补充数据的标准json 补充完整
    getKeyPoint_fromPic.write_standard_data2json(key_point, 'Standard')



# vedio_path: 视频路径
# out_dir: 输出图片路径
# TODO: 取出视频中start_time到end_time中间的n帧，转为图片
def video2JpgProcess(video_path, out_dir, start_time, end_time, data_list_name):

    with open('Data/' + data_list_name + '.json', 'r')as f:  # 打开这个动作的标准数据json
        standard_data = json.load(f)  # 读取这个json里所有的数据

        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        cap = cv2.VideoCapture(video_path)  # 到时用摄像头就换这里
        filename = os.path.basename(video_path).split(".")[0]   # 把视频名截取出来
        countReadFrame = start_time
        while countReadFrame <= end_time*24:
            r, frame = cap.read()  # frame是那一帧
            if r:
                # 下面一行是控制每秒的帧数
                if countReadFrame % 12 != 0:
                    countReadFrame = countReadFrame + 1
                    continue

                outname = "{}-{}.jpg".format(filename, str(countReadFrame).zfill(3))
                outPath = os.path.join(out_dir, outname)
                cv2.imwrite(outPath, frame)
                cv2.imencode('.jpg', frame)[1].tofile(outPath)  # 从内存转到磁盘存下来
                countReadFrame = countReadFrame + 1
                print(outname)

                key_point = [[[[0.0] for i in range(2)] for j in range(2)] for k in range(22)]  # 身体关键点数组
                lineup = [[1, 2], [0, 5], [5, 8], [8, 15], [15, 17], [17, 19], [8, 16], [16, 18],  # 身体关键点两两连线
                          [18, 20], [8, 9], [9, 11], [11, 13], [8, 10], [10, 12], [12, 14]]
                # TODO: 如果检测到没人就跳过该帧，如果有人就进行识别
                try:
                    flag = getKeyPoint_fromPic.getkp_fpicture(key_point, frame)
                    if flag:
                        continue
                    else:
                        judgeAction.jdg_if_correct(standard_data, key_point)
                except KeyError:
                    print("识别到没人")

                # 从特定图片中获得人体关键点
            else:
                break
            if cv2.waitKey(1) & 0xFF == ord("q"):  # Exit condition
                break


def pre_process(key_point, train_img):
    # TODO：拍摄/获取用户全身照and预处理
    # 实际应用中，需要持续捕捉用户全身照，直到符合标准为止
    # whole_body_pic_name = 'whole_body'
    # pic_file_location = './img_input/' + whole_body_pic_name + '.jpg'
    # whole_body_pic = cv2.imread(pic_file_location)
    getKeyPoint_fromPic.getkp_fpicture(key_point, train_img)
    # print(train_img)
    # skeleton_length = getKeyPoint_fromPic.cal_skeleton_length(lineup, key_point, train_img)  # 骨架长度

    # TODO: 将该训练的所有需要新补充数据的标准json 补充完整
    getKeyPoint_fromPic.write_standard_data2json(key_point, 'Standard')


# TODO: 读取训练标准集，
if __name__ == '__main__':
    '''
    sinscry
    关于初始化数据，和开启线程
    '''
    # EMG_data = array.array('d')  # 可动态改变数组的大小,double型数组
    # historyLength = 500  # 横坐标长度
    # S_or_E = 0
    # th1 = threading.Thread(target=Serial)#目标函数一定不能带（）被这个BUG搞了好久
    # th1.start()

# ——————————————————————————————————————————————————————————————————————————————————————————

    # TODO： 传入视频，现在先以视频文件的形式，如果需要再改成cap from camera
    # video_name = 'Section1'
    # video_path = 'videos/' + video_name + '.mp4'
    # out_dir = 'img_input/'
    cap = cv2.VideoCapture(0)  # 从摄像头读取

    key_point = [[[0.0, 0.0] for j in range(2)] for k in range(22)]  # 身体关键点数组
    lineup = [[1, 2], [0, 5], [5, 8], [8, 15], [15, 17], [17, 19], [8, 16], [16, 18],  # 身体关键点两两连线
              [18, 20], [8, 9], [9, 11], [11, 13], [8, 10], [10, 12], [12, 14]]

    # TODO：打开动作训练List，获得每个训练集的名字、开始时间和结束时间
    with open('Data/List.json', 'r')as f:
        data_index = 0
        data_list = json.load(f)
        keys = list(data_list.keys())
        data_list_name = keys[data_index]
        start_time = data_list[data_list_name][0]
        end_time = data_list[data_list_name][1]
        with open('Data/' + data_list_name + '.json', 'r')as f1:
            standard_data = json.load(f1)

        # for data_list_name in data_list:  # 训练动作的标准数据的 名字

        # TODO：检测用户是哪侧面对镜头，将该侧的数据标准写入标准集.json里

        # TODO：开始检测
        # if not os.path.exists(out_dir):
        #     os.makedirs(out_dir)
        # cap = cv2.VideoCapture(video_path)  # 到时用摄像头就换这里
        # cap = cv2.VideoCapture(0)
        # cap = camera.read()

        # filename = os.path.basename(video_path).split(".")[0]  # 把视频名截取出来
        now1 = time.time()
        last_time = 0  # 识别上一帧的时间
        while True:
            if not cap.isOpened():
                continue
            r, frame = cap.read()  # frame是那一帧
            if not r:
                continue
            frame = cv2.resize(frame, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)
            if cv2.waitKey(1) & 0xFF == ord("q"):  # Exit condition
                break
            elif r:
                # 下面一行是控制每秒的帧数
                # if countReadFrame % 12 != 0:
                #     countReadFrame = countReadFrame + 1
                #     continue

                # 输出该帧识别后的图像，保存到文件夹里
                # outname = "{}-{}.jpg".format(filename, str(countReadFrame).zfill(3))
                # outPath = os.path.join(out_dir, outname)
                # cv2.imwrite(outPath, frame)
                # cv2.imencode('.jpg', frame)[1].tofile(outPath)  # 从内存转到磁盘存下来
                # countReadFrame = countReadFrame + 1
                # print(outname)
                now = time.time() - now1  # 现在识别这一帧的时间
                # print('{} {} {} {} {}'.format(now, last_time, start_time, end_time, time.time()-last_time))
                if now > end_time:  # 结束了该动作的比对
                    print("准备下一组动作的识别")
                    data_index += 1
                    data_list_name = keys[data_index]
                    start_time = data_list[data_list_name][0]
                    end_time = data_list[data_list_name][1]
                    with open('Data/' + data_list_name + '.json', 'r')as f1:
                        standard_data = json.load(f1)
                        print(data_list_name)
                elif now >= start_time and EMG_determine()==1:  # and肌电传感器那里说ready，开始对该动作的对比  【and now - last_time > 0.5，先继续保持注释】
                    print("开始识别")
                    print('{} {} {} {}'.format(now, last_time, start_time, end_time))
                    last_time = now
                    print(data_list_name)
                    # TODO: 如果检测到没人就跳过该帧，如果有人就进行识别
                    try:
                        # print("进来识别了！！！")
                        flag = getKeyPoint_fromPic.getkp_fpicture(key_point, frame)
                        if flag:
                            continue
                        else:
                            judgeAction.jdg_if_correct(standard_data, key_point)
                    except KeyError:
                        print("识别到没人")
                cv2.imshow('video', frame)
            else:
                break

        cv2.destroyWindow('MyCamera')

    # with open('Data/List.json', 'r')as f:
    #     data_list = json.load(f)
    #     for data_list_name in data_list:  # 训练动作的标准数据的 名字
    #         start_time = data_list[data_list_name][0]
    #         end_time = data_list[data_list_name][1]
            # video2JpgProcess(video_path, out_dir, start_time, end_time, data_list_name)


