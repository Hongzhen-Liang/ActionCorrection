import requests
import base64
import cv2, os
import numpy as np
import matplotlib.pyplot as plt
import getKeyPoint_fromPic
import judgeAction
import json
import cmath

# TODO：识别人体关键点并记录
# 1. 读取视频
# 2. 将视频的每一帧（或者每秒取12帧）取出来
# 3. 放到API去识别人体关键点
# 4. 返回KEY POINTS数据
# 5. 将数据写入txt文件

# video_filename = 'E:/ActionCorrection/videos/YogaCoachVideo1.mp4'
# out_dir = 'E:/ActionCorrectio/images

if __name__ == '__main__':
    # TODO: 1. 得到该图像的关键点坐标，并保存到txt文件里
    #       2. 将关键点画到该图上，并连线
    pic_name = 'try111'  # 这是我输入的这次要识别的图像
    Key_Point = [[[0.0, 0.0] for j in range(2)] for k in range(22)]  # 身体关键点数组
    lineup = [[1, 2], [0, 5], [5, 8], [8, 15], [15, 17], [17, 19], [8, 16], [16, 18],  # 身体关键点两两连线
              [18, 20], [8, 9], [9, 11], [11, 13], [8, 10], [10, 12], [12, 14]]
    getKeyPoint_fromPic.getkp_fpicture(Key_Point, pic_name)  # 从特定图片中获得人体关键点
    # Selected_KeyParts[i][选中与否，0-未选中，1-算角度，2-算相对距离] = 距离
    # TODO: 读取List.json，得到训练动作标准集与开始、结束时间
    with open('Data/List.json', 'r')as f:
        running_list = json.load(f)

    # TODO: 读取 Standard.json 里的数据，并判断是否符合标准
    with open('Data/CatStretch.json', 'r')as f:
        standard_data = json.load(f)
    # TODO：利用json内的标准数据，判断用户动作是否正确
    for key in standard_data:
        if key == 'angle':
            for point_key in standard_data[key]:
                related_points = [int(i) for i in point_key.split(',')]
                realtime_angle = judgeAction.cal_angle(Key_Point[related_points[0]], Key_Point[related_points[1]],
                                                       Key_Point[related_points[2]], Key_Point[related_points[3]])
                angle_scope = standard_data[key][point_key]
                if angle_scope[0] <= realtime_angle <= angle_scope[1]:  # 符合
                    print("伸直了！" + str(realtime_angle))
                else:  # 不符合
                    print("该肢没有伸直" + str(realtime_angle))
        elif key == 'distance':
            for point_key in standard_data[key]:
                tmp = point_key.split('-')
                # bg_point = int(tmp[0])  # 某个关节点
                bg_point = Key_Point[int(tmp[0])][0]  # 该点的x,y值的list
                # target_point = int(tmp[1])
                target_point = Key_Point[int(tmp[1])][0]
                type1 = tmp[-1]
                judgeAction.cal_if_located(target_point, bg_point, type1, standard_data[key][point_key])


    # selected_keyparts = [[0]for i in range(15)]  # 选中身体关键部位
    # usage_skeyparts = [[0.0]for i in range(15)]  # 如何使用（角度/相对范围）选中的身体关键部位

    # TODO： 确定该动作的关键身体部位
    # print('请输入该动作的关键身体部位(输入空格隔开，回车结束)：')
    # print('提示：头：0  右左眼12  右左耳34  鼻子5  右左嘴67  脖子8\n'
    #       '右左肩9 10  右左手肘11 12  右左手腕13 14  右左屁股15 16  右左膝盖17 18  右左脚踝19 20\n')
    # list1 = []  # 用户输入的整数（关键部位）列表
    # str1 = input()
    # list2 = str1.split(" ")  # 储存输入的字符串，用空格分开 !!!注意：这里只有一个空格，如果输入的时候有两个及以上的情况（因为之后可能用点击来搞，先不管）
    # i = 0
    # for i in range(len(list2)):
    #     list1.append(int(list2.pop()))  # 将list2里的数据转换为整型并赋值给list1

    # print(list1) # 注意：list1里的数据与输入时的顺序相反
    # item successfully input list1
    # way1:
    # for item in list1:  #  这样输出的顺序与输入相反
    #     print(item)
    # way2:
    # j = 0   # 这样输出的顺序与输入相同
    # for j in range(i+1):
    #     print(list1.pop())

    # TODO: 判断动作正确与否
    #     思路1： 用教练的身体数据直接进行比对（设置误差值）
    #     思路2： 用我们设置的正确标准进行判断

    #  TODO： 现打算实现思路1
    #    预备：拿到本次动作关键部位是哪几个的数据list1
    #    1 读取教练完成这个动作的关键点数据
    #      包括教练的身体骨架比例（这个就先记录进文件里，直接读取）
    #    2.让学员先拍一个静止的、无遮挡的全身图
    #    3.将教练身体比例放缩成学员大小，即把完成动作的标准的数据改成适合学员的
    #    4.进行学员与之标准动作进行对比

    # TODO: 对比两张图的关键点
    # TODO： 先将标准动作的角度弄出来
    # sf = 'E: / ActionCorrection / keypoints_data / ' + pic_name + '.txt'
    # standard_file = open(sf)
