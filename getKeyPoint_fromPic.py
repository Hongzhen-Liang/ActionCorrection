import base64
import cv2
import os
import requests
import numpy as np
import json
import judgeAction
import array
from util import frame2base64

body_words = [
    'top_head',
    'right_eye', 'left_eye',
    'right_ear', 'left_ear',
    'nose',
    'right_mouth_corner', 'left_mouth_corner',
    'neck',
    'right_shoulder', 'left_shoulder',
    'right_elbow', 'left_elbow',
    'right_wrist', 'left_wrist',
    'right_hip', 'left_hip',
    'right_knee', 'left_knee',
    'right_ankle', 'left_ankle'
]


def getkp_fpicture(key_point, img):
    if img is None:
        return None
    if key_point is None:
        key_point = [[[0.0, 0.0] for j in range(2)] for k in range(22)]  # 身体关键点数组
    # 连接百度识别人体关键点API
    client_id = 'TLVn4rr4ULC1VaoFPcrfu0wh'  # API Key
    client_secret = '7u79YRo0c7OkGGVMfa1mGLp2tzqSC38r'  # Secret Key

    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}' \
        .format(client_id, client_secret)
    response1 = requests.post(host)
    access_token = response1.json()['access_token']
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_analysis?access_token=" + access_token
    response2 = requests.post(request_url, data={"image": frame2base64(img)})

    # TODO: 把key_point写入数组
    # top_head:0
    # right_eye:1  left_eye:2
    # right_ear:3  left_ear:4
    # nose:5
    # right_mouth_corner:6  left_mouth_corner:7
    # neck:8
    # right_shoulder:9  left_shoulder:10
    # right_elbow:11  left_elbow:12
    # right_wrist:13  left_wrist:14
    # right_hip:15  left_hip：16
    # right_knee：17  left_knee：18
    # right_ankle：19  left_ankle：20
    # location：21 [width][height][score]{ width/ top / score /left /height}
    # log id [dk是否有用]

    humans = response2.json()
    # 如果监测到的人数=0，就返回（去下一帧继续检测）
    try:
        if humans['person_num'] == 0:
            return None
    except KeyError:
        return None

    print("得到人体关键点数据~~~")

    global body_words
    for i in range(len(body_words)):
        key_point[i][0][0] = humans['person_info'][0]['body_parts'][body_words[i]]['x']
        key_point[i][0][1] = humans['person_info'][0]['body_parts'][body_words[i]]['y']
        key_point[i][1][0] = round(humans['person_info'][0]['body_parts'][body_words[i]]['score'], 2)
        key_point[i][1][1] = 0  # 作flag（0：不参与比较；1：参与比较）

    key_point[len(body_words)][0][0] = humans['person_info'][0]['location']['width']
    key_point[len(body_words)][0][1] = humans['person_info'][0]['location']['height']
    key_point[len(body_words)][1][0] = round(humans['person_info'][0]['location']['score'], 2)
    key_point[len(body_words)][1][1] = 0

    # TODO: 将key_points写入txt文件【给教练数据用】
    # kpfilename = 'E:/ActionCorrection/kp_coordinate/' + pic_name + '.txt'
    # if not os.path.isfile(kpfilename):
    #     file = open(kpfilename, 'a', encoding="utf-8")
    # else:
    #     file = open(kpfilename, 'w', encoding="utf-8")
    #
    # for i in range(22):
    #     for j in range(2):
    #         for k in range(2):
    #             s = str(key_point[i]).replace('[', '').replace(']', '') + '\n'
    #     file.write(s)
    # file.close()
    # print("保存关节点文件成功！")

    # # TODO: 将骨架长度写入txt文件
    #         如果要保存文件，用cal_skeleton_length(lineup, key_point, image1)函数return的值
    # skelen_resultlocation = './kp_proportion/' + pic_name + '.txt'
    # if not os.path.isfile(skelen_resultlocation):
    #     file = open(skelen_resultlocation, 'a', encoding="utf-8")
    # else:
    #     file = open(skelen_resultlocation, 'w', encoding="utf-8")
    # for i in range(15):
    #     s = str(i) + '.' + str(skeleton_length[i]) + '\n'
    #     file.write(s)
    # file.close()
    # print("保存骨架长度数据文件成功！")

    # pic_resultlocation = './img_result/' + pic_name + '.jpg'
    # cv2.imwrite(pic_resultlocation, image1)
    # cv2.imshow('result', image1)
    # print("保存结果图片成功！")

    return key_point  # 检测到人


# TODO: 计算各段骨架长度
def cal_skeleton_length(lineup, key_point, image1):
    skeleton_length = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 骨架长度
    j = 0
    for i in lineup:
        x1 = np.float32(key_point[i[0]][0][0])
        y1 = np.float32(key_point[i[0]][0][1])
        x2 = np.float32(key_point[i[1]][0][0])
        y2 = np.float32(key_point[i[1]][0][1])
        cv2.line(image1, (x1, y1), (x2, y2), (0, 0, 255), 3)
        # if i[0] == 9:  # 图片里人自己的左右就是这里的左右
        #     cv2.line(Image1, (x1, y1), (x2, y2), (255, 255, 0), 5)
        ske_temp = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)  # 算出每段骨架的长度
        skeleton_length[j] = round(ske_temp, 2)  # 将长度四舍五入
        j += 1
    return skeleton_length


# TODO：判断用户身体的左侧/右侧对着镜头
# 判断方式：判断左耳/右耳的准确率，谁高就是哪边；若都低于0.25就重新取帧，若都高于0.85，则是正面（否决）
# 判断方式：左/右边（躯干）平均识别准确率哪边高就是哪边[即使挑出需要检测的部位，但只有66.7%左右的正确率]
def jdg_side(key_point, num):
    right_percentage = 0
    left_percentage = 0
    # i = 9
    i = num
    for i in range(num, 20, 2):
        right_percentage += key_point[i][1][0]
    right_percentage = right_percentage
    i = num+1
    for i in range(num+1, 21, 2):
        left_percentage += key_point[i][1][0]
    left_percentage = left_percentage
    if right_percentage >= left_percentage:
        return 1  # 1为右边
    else:
        return 2  # 2为左边


# 将需要预先处理的数据（数据集名称：关键点 数据）按标准集json的规格写进
# # TODO：将需要的数据写入标准集.json
def write_standard_data2json(key_point, standard_name):
    with open('Data/' + standard_name + '.json', 'r')as f:
        standard = json.load(f)
        for standard_list_name in standard:  # 动作标准集的名字（如DownDog）
            with open('Data/' + standard_list_name + '.json', 'r+')as f2:  # 打开了该标准集
                this_standard = json.load(f2)
                for key in standard[standard_list_name]:  # 该集内的判断方向（distance/angel）
                    for kp_dis in standard[standard_list_name][key]:  # 关键点位置
                        # 将该数据集里对应位置的数据填上
                        # this_standard = {
                        #     standard[standard_name][key]:{
                        #         kp_dis:[result1,result2]}
                        # }
                        if key == "distance":
                            kp_temp = kp_dis.split('-')
                            if len(kp_temp) == 3:
                                i = 0
                                j = 1
                            elif len(kp_temp) == 5:
                                i = 3
                                j = 4
                            if kp_temp[2] == 'x':
                                x1 = key_point[int(kp_temp[i])][0][0]
                                x2 = key_point[int(kp_temp[j])][0][0]
                                skeleton_length = x1 - x2
                            elif kp_temp[2] == 'y':
                                y1 = key_point[int(kp_temp[i])][0][1]
                                y2 = key_point[int(kp_temp[j])][0][0]
                                skeleton_length = y1 - y2
                            elif kp_temp[2] == 'r':
                                x1 = key_point[int(kp_temp[i])][0][0]
                                x2 = key_point[int(kp_temp[j])][0][0]
                                y1 = key_point[int(kp_temp[i])][0][1]
                                y2 = key_point[int(kp_temp[j])][0][0]
                                skeleton_length = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

                            # 原始标准数据集，如果是需要用骨架长度的，就不用写数据
                            result1 = skeleton_length - standard[standard_list_name][key][kp_dis][0]  # 误差1（较小的）
                            result2 = skeleton_length + standard[standard_list_name][key][kp_dis][1]  # 误差2（较大的）
                            this_standard[key][kp_dis] = [result1, result2]
                        elif key == "angle":
                            kp_temp = [int(i) for i in kp_dis.split(',')]
                            p1 = key_point[kp_temp[0]]
                            p2 = key_point[kp_temp[1]]
                            q1 = key_point[kp_temp[2]]
                            q2 = key_point[kp_temp[3]]
                            user_angle = judgeAction.cal_angle(p1, p2, q1, q2)
                            # 原始标准数据集，写好标准范围，如果需要使用 用户原本身体的自然夹角，如下【standard那无需写数据】
                            angle_result1 = this_standard[key][kp_dis][0] - user_angle
                            angle_result2 = this_standard[key][kp_dis][1] + user_angle
                            this_standard[key][kp_dis] = [angle_result1, angle_result2]
                write_this_standard = json.dumps(this_standard, indent=2)
            with open('Data/' + standard_list_name + '.json', 'w')as f2:  # 打开了该标准集
                f2.write(write_this_standard)
                print("写入json文件成功")


lineup = [[1, 2], [0, 5], [5, 8], [8, 15], [15, 17], [17, 19], [8, 16], [16, 18],
          [18, 20], [8, 9], [9, 11], [11, 13], [8, 10], [10, 12], [12, 14]]


def draw_human(img, key_point, key_point_color):
    if key_point is None:
        return
    # 将点点画到图片上
    for i in range(21):  # 画点
        x = int(key_point[i][0][0])
        y = int(key_point[i][0][1])
        # cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]])
        cv2.circle(img, (x, y), 2, key_point_color[i], -1)
    # print("成功画点！")
    # 点连成线，并画出来
    # TODO：计算身体比例（身体每段骨架的长度）
    # skeleton_length = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 骨架长度
    global lineup
    # j = 0
    for i in lineup:
        x1, y1 = np.float32(key_point[i[0]][0][0]), np.float32(key_point[i[0]][0][1])
        x2, y2 = np.float32(key_point[i[1]][0][0]), np.float32(key_point[i[1]][0][1])
        cv2.line(img, (x1, y1), (x2, y2), key_point_color[i[0]], 3)
        # if i[0] == 9:  # 图片里人自己的左右就是这里的左右
        #     cv2.line(Image1, (x1, y1), (x2, y2), (255, 255, 0), 5)
        # ske_temp = np.sqrt((x1-x2)**2 + (y1-y2)**2)  # 算出每段骨架的长度
        # skeleton_length[j] = round(ske_temp, 2)  # 将长度四舍五入
        # j += 1
