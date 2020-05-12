import base64
from util import frame2base64
import requests
import os
import cv2
import numpy as np
import getKeyPoint_fromPic
import judgeAction

if __name__ == '__main__':
    img_name = "RightFancyChairTwist_RIGHT9"
    pic_file_location = './img_input/' + img_name + '.jfif'
    f = open(pic_file_location, 'rb')
    img2 = f.read()
    img3 = cv2.imread(pic_file_location)
    img1 = base64.b64encode(img2)
    img = cv2.UMat(img3)
    # img1 = frame2base64(img)
    # 连接百度识别人体关键点API
    client_id = 'TLVn4rr4ULC1VaoFPcrfu0wh'  # API Key
    client_secret = '7u79YRo0c7OkGGVMfa1mGLp2tzqSC38r'  # Secret Key
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}' \
        .format(client_id, client_secret)
    response1 = requests.post(host)
    print(response1.json())
    access_token = response1.json()['access_token']
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_analysis?access_token=" + access_token
    data = {"image": img1}
    response2 = requests.post(request_url, data=data)
    # print(type(response2.json()['person_info']))
    print(response2.json())
    humans = response2.json()


    key_point = [[[0.0, 0.0] for j in range(2)] for k in range(22)]
    lineup = [[1, 2], [0, 5], [5, 8], [8, 15], [15, 17], [17, 19], [8, 16], [16, 18],  # 身体关键点两两连线
              [18, 20], [8, 9], [9, 11], [11, 13], [8, 10], [10, 12], [12, 14]]

    key_point[0][0][0] = humans['person_info'][0]['body_parts']['top_head']['x']
    key_point[0][0][1] = humans['person_info'][0]['body_parts']['top_head']['y']
    key_point[0][1][0] = round(humans['person_info'][0]['body_parts']['top_head']['score'], 2)
    key_point[0][1][1] = 0  # 作flag（0：不参与比较；1：参与比较）

    key_point[1][0][0] = humans['person_info'][0]['body_parts']['right_eye']['x']
    key_point[1][0][1] = humans['person_info'][0]['body_parts']['right_eye']['y']
    key_point[1][1][0] = round(humans['person_info'][0]['body_parts']['right_eye']['score'], 2)
    key_point[1][1][1] = 0

    key_point[2][0][0] = humans['person_info'][0]['body_parts']['left_eye']['x']
    key_point[2][0][1] = humans['person_info'][0]['body_parts']['left_eye']['y']
    key_point[2][1][0] = round(humans['person_info'][0]['body_parts']['left_eye']['score'], 2)
    key_point[2][1][1] = 0

    key_point[3][0][0] = humans['person_info'][0]['body_parts']['right_ear']['x']
    key_point[3][0][1] = humans['person_info'][0]['body_parts']['right_ear']['y']
    key_point[3][1][0] = round(humans['person_info'][0]['body_parts']['right_ear']['score'], 2)
    key_point[3][1][1] = 0

    key_point[4][0][0] = humans['person_info'][0]['body_parts']['left_ear']['x']
    key_point[4][0][1] = humans['person_info'][0]['body_parts']['left_ear']['y']
    key_point[4][1][0] = round(humans['person_info'][0]['body_parts']['left_ear']['score'], 2)
    key_point[4][1][1] = 0

    key_point[5][0][0] = humans['person_info'][0]['body_parts']['nose']['x']
    key_point[5][0][1] = humans['person_info'][0]['body_parts']['nose']['y']
    key_point[5][1][0] = round(humans['person_info'][0]['body_parts']['nose']['score'], 2)
    key_point[5][1][1] = 0

    key_point[6][0][0] = humans['person_info'][0]['body_parts']['right_mouth_corner']['x']
    key_point[6][0][1] = humans['person_info'][0]['body_parts']['right_mouth_corner']['y']
    key_point[6][1][0] = round(humans['person_info'][0]['body_parts']['right_mouth_corner']['score'], 2)
    key_point[6][1][1] = 0

    key_point[7][0][0] = humans['person_info'][0]['body_parts']['left_mouth_corner']['x']
    key_point[7][0][1] = humans['person_info'][0]['body_parts']['left_mouth_corner']['y']
    key_point[7][1][0] = round(humans['person_info'][0]['body_parts']['left_mouth_corner']['score'], 2)
    key_point[7][1][1] = 0

    key_point[8][0][0] = humans['person_info'][0]['body_parts']['neck']['x']
    key_point[8][0][1] = humans['person_info'][0]['body_parts']['neck']['y']
    key_point[8][1][0] = round(humans['person_info'][0]['body_parts']['neck']['score'], 2)
    key_point[8][1][1] = 0

    key_point[9][0][0] = humans['person_info'][0]['body_parts']['right_shoulder']['x']
    key_point[9][0][1] = humans['person_info'][0]['body_parts']['right_shoulder']['y']
    key_point[9][1][0] = round(humans['person_info'][0]['body_parts']['right_shoulder']['score'], 2)
    key_point[9][1][1] = 0

    key_point[10][0][0] = humans['person_info'][0]['body_parts']['left_shoulder']['x']
    key_point[10][0][1] = humans['person_info'][0]['body_parts']['left_shoulder']['y']
    key_point[10][1][0] = round(humans['person_info'][0]['body_parts']['left_shoulder']['score'], 2)
    key_point[10][1][1] = 0

    key_point[11][0][0] = humans['person_info'][0]['body_parts']['right_elbow']['x']
    key_point[11][0][1] = humans['person_info'][0]['body_parts']['right_elbow']['y']
    key_point[11][1][0] = round(humans['person_info'][0]['body_parts']['right_elbow']['score'], 2)
    key_point[11][1][1] = 0

    key_point[12][0][0] = humans['person_info'][0]['body_parts']['left_elbow']['x']
    key_point[12][0][1] = humans['person_info'][0]['body_parts']['left_elbow']['y']
    key_point[12][1][0] = round(humans['person_info'][0]['body_parts']['left_elbow']['score'], 2)
    key_point[12][1][1] = 0

    key_point[13][0][0] = humans['person_info'][0]['body_parts']['right_wrist']['x']
    key_point[13][0][1] = humans['person_info'][0]['body_parts']['right_wrist']['y']
    key_point[13][1][0] = round(humans['person_info'][0]['body_parts']['right_wrist']['score'], 2)
    key_point[13][1][1] = 0

    key_point[14][0][0] = humans['person_info'][0]['body_parts']['left_wrist']['x']
    key_point[14][0][1] = humans['person_info'][0]['body_parts']['left_wrist']['y']
    key_point[14][1][0] = round(humans['person_info'][0]['body_parts']['left_wrist']['score'], 2)
    key_point[14][1][1] = 0

    key_point[15][0][0] = humans['person_info'][0]['body_parts']['right_hip']['x']
    key_point[15][0][1] = humans['person_info'][0]['body_parts']['right_hip']['y']
    key_point[15][1][0] = round(humans['person_info'][0]['body_parts']['right_hip']['score'], 2)
    key_point[15][1][1] = 0

    key_point[16][0][0] = humans['person_info'][0]['body_parts']['left_hip']['x']
    key_point[16][0][1] = humans['person_info'][0]['body_parts']['left_hip']['y']
    key_point[16][1][0] = round(humans['person_info'][0]['body_parts']['left_hip']['score'], 2)
    key_point[16][1][1] = 0

    key_point[17][0][0] = humans['person_info'][0]['body_parts']['right_knee']['x']
    key_point[17][0][1] = humans['person_info'][0]['body_parts']['right_knee']['y']
    key_point[17][1][0] = round(humans['person_info'][0]['body_parts']['right_knee']['score'], 2)
    key_point[17][1][1] = 0

    key_point[18][0][0] = humans['person_info'][0]['body_parts']['left_knee']['x']
    key_point[18][0][1] = humans['person_info'][0]['body_parts']['left_knee']['y']
    key_point[18][1][0] = round(humans['person_info'][0]['body_parts']['left_knee']['score'], 2)
    key_point[18][1][1] = 0

    key_point[19][0][0] = humans['person_info'][0]['body_parts']['right_ankle']['x']
    key_point[19][0][1] = humans['person_info'][0]['body_parts']['right_ankle']['y']
    key_point[19][1][0] = round(humans['person_info'][0]['body_parts']['right_ankle']['score'], 2)
    key_point[19][1][1] = 0

    key_point[20][0][0] = humans['person_info'][0]['body_parts']['left_ankle']['x']
    key_point[20][0][1] = humans['person_info'][0]['body_parts']['left_ankle']['y']
    key_point[20][1][0] = round(humans['person_info'][0]['body_parts']['left_ankle']['score'], 2)
    key_point[20][1][1] = 0

    key_point[21][0][0] = humans['person_info'][0]['location']['width']
    key_point[21][0][1] = humans['person_info'][0]['location']['height']
    key_point[21][1][0] = round(humans['person_info'][0]['location']['score'], 2)
    key_point[21][1][1] = 0

    # TODO: 将key_points写入txt文件【给教练数据用】
    kpfilename = 'E:/ActionCorrection/kp_coordinate/' + img_name + '.txt'
    if not os.path.isfile(kpfilename):
        file = open(kpfilename, 'a', encoding="utf-8")
    else:
        file = open(kpfilename, 'w', encoding="utf-8")

    for i in range(22):
        for j in range(2):
            for k in range(2):
                s = str(key_point[i]).replace('[', '').replace(']', '') + '\n'
        file.write(s)
    file.close()
    print("保存关节点文件成功！")

    # TODO: 连线用的,将点点画到图片上
    for i in range(21):  # 画点
        x = int(key_point[i][0][0])
        y = int(key_point[i][0][1])
        # cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]])
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
        if i == 9:
            cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
        if i == 10:
            cv2.circle(img, (x, y), 10, (255, 255, 0), -1)
        if i == 17:
            cv2.circle(img, (x, y), 10, (255, 255, 255), -1)
    print("成功画点！")

    for i in lineup:
        x1 = np.float32(key_point[i[0]][0][0])
        y1 = np.float32(key_point[i[0]][0][1])
        x2 = np.float32(key_point[i[1]][0][0])
        y2 = np.float32(key_point[i[1]][0][1])
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
        # if i[0] == 9:  # 图片里人自己的左右就是这里的左右
        #     cv2.line(img, (x1, y1), (x2, y2), (255, 255, 0), 5)

    pic_resultlocation = './img_result/' + img_name + '.jpg'
    cv2.imwrite(pic_resultlocation, img)
    cv2.imshow('result', img)
    print("保存结果图片成功！")

    # num = 9  # 从该节点开始比对识别率
    # flag = getKeyPoint_fromPic.jdg_side(key_point,num)
    # if flag == 1:
    #     print("right")
    # elif flag == 2:
    #     print("left")

    # TODO:计算手肘离膝盖的距离
    # if key_point[17][1][0] >= key_point[18][1][0]:
    #     bg = key_point[18][0]
    # else:
    #     bg = key_point[17][0]
    # tg = key_point[11][0]
    # judgeAction.cal_if_located(tg, bg, 'r', [0, 40])

    # TODO:计算上边的肩膀和手腕的垂直距离
    if key_point[9][0][1] <= key_point[10][0][1]:
        tg = key_point[13][0]
        bg = key_point[9][0]
        print("hei")
    else:
        tg = key_point[14][0]
        bg = key_point[10][0]
    judgeAction.cal_if_located(tg, bg, 'y', [0, 100])