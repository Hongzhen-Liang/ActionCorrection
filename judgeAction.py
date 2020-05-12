import cmath
import math

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
kp_tips = {
    0: "头顶",
    1: "右眼", 2: "左眼",
    3: "右耳", 4: "左耳",
    5: "鼻子",
    6: "右嘴角", 7: "左嘴角",
    8: "脖子",
    9: "右肩膀", 10: "左肩膀",
    11: "右手肘", 12: "左手肘",
    13: "右手腕", 14: "左手腕",
    15: "右屁股", 16: "左屁股",
    17: "右膝盖", 18: "左膝盖",
    19: "右脚踝", 20: "左脚踝"
}


# TODO: 计算两条线段(vector)之间的角度
def cal_angle(p1, p2, q1, q2):
    x1, y1 = p1[0][0], p1[0][1]
    x2, y2 = p2[0][0], p2[0][1]
    x3, y3 = q1[0][0], q1[0][1]
    x4, y4 = q2[0][0], q2[0][1]
    vx1 = x2 - x1
    vy1 = y2 - y1
    vx2 = x4 - x3
    vy2 = y4 - y3
    up = vx1 * vx2 + vy1 * vy2
    down = abs(cmath.sqrt(vx1 * vx1 + vy1 * vy1)) * abs(cmath.sqrt(vx2 * vx2 + vy2 * vy2))
    if down == 0:
        return -1
    cos = round(up / down, 2)  # cosα的数值[-1,1]
    return math.acos(cos) * 180 / math.pi  # α的角度


# TODO: 计算选中关节点形成的夹角
#       现令key_point[i][1][1] = 2 时，需要计算角度
# def cal_data(key_point, selected_keyparts):
#     for i in range(15):
#         if selected_keyparts[i] == 0:  # 没有被选
#             continue
#         elif selected_keyparts[i] == 1:   # 选中，计算角度
#             cal_angle(key_point[i])
#         else:  # 选中，计算相对距离
#             usage_skeyparts[i]


# TODO： 计算目标点是否在某范围内
def cal_if_located(target_point, location_point, _type, distance):
    if _type == 'x':
        now_dis = target_point[0] - location_point[0]
        if distance[0] <= now_dis <= distance[1]:
            return "ok!"
        else:
            if distance[0] == -distance[1]:
                return kp_tips[target_point[2]]+"与"+kp_tips[location_point[2]]+"要保持垂直"
            elif now_dis < distance[0]:
                return "请增大"+kp_tips[target_point[2]]+"与"+kp_tips[location_point[2]]+"的距离"
            elif now_dis > distance[1]:
                return "请减小" + kp_tips[target_point[2]] + "与" + kp_tips[location_point[2]] + "的距离"
    elif _type == 'y':
        now_dis = target_point[1] - location_point[1]
        if distance[0] <= now_dis <= distance[1]:
            return "ok!"
        else:
            if distance[0] == -distance[1]:
                return "放平"+kp_tips[target_point[2]]+"与"+kp_tips[location_point[2]]+"的距离"
            elif now_dis < distance[0]:
                return "请提高"+kp_tips[target_point[2]]+"的位置"
            elif now_dis > distance[1]:
                return "请降低"+kp_tips[target_point[2]]+"的位置"
    else:  # 半径范围内
        x1 = target_point[0]
        y1 = target_point[1]
        x2 = location_point[0]
        y2 = location_point[1]
        r = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        if distance[0] <= r <= distance[1]:
            return "okk!!"
        else:
            if r < distance[0]:
                return "请伸直"+kp_tips[target_point[2]]+"与"+kp_tips[location_point[2]]
            elif r > distance[1]:
                return "请缩短"+kp_tips[target_point[2]]+"与"+kp_tips[location_point[2]]+"的距离"


# TODO： 通过骨架长度的变化，计算其关节在三维环境中移动的角度（距离）
def cal_line_lengthchange(standard_data, realtime_data):
    for s_key in standard_data.keys:
        # standard_data[s_key]
        pass


def jdg_if_correct(standard_data, key_point, key_point_color):
    """
    利用json内的标准数据，判断用户动作是否正确
    :param key_point_color:
    :param standard_data:
    :param key_point:
    :return: 错误信息字符串
    """
    if key_point is None:
        return ""
    for key in standard_data:
        if key == 'angle':
            for point_key in standard_data[key]:
                related_points = [int(i) for i in point_key.split(',')]
                realtime_angle = cal_angle(key_point[related_points[0]], key_point[related_points[1]],
                                           key_point[related_points[2]], key_point[related_points[3]])
                angle_scope = standard_data[key][point_key]
                if angle_scope[0] <= realtime_angle <= angle_scope[1]:  # 符合
                    for i in [0, 1, 3]:
                        key_point_color[related_points[i]] = (0, 0, 255)
                    return "{0[0]}与{0[1]}、{0[2]}形成的角度正确".format([kp_tips[related_points[i]] for i in [0, 1, 3]])
                    # print("伸直了！" + str(realtime_angle))
                else:  # 不符合
                    for i in [0, 1, 3]:
                        key_point_color[related_points[i]] = (255, 0, 0)
                    if angle_scope[0] <= 180 <= angle_scope[1]:
                        return "请保持{0[0]}与{0[1]}和{0[2]}成一条直线".format([kp_tips[related_points[i]] for i in [0, 1, 3]])
                    elif realtime_angle < angle_scope[0]:
                        return "请扩大{0[0]}与{0[1]}和{0[2]}的角度".format([kp_tips[related_points[i]] for i in [0, 1, 3]])
                    elif realtime_angle > angle_scope[1]:
                        return "请减小{0[0]}与{0[1]}和{0[2]}的角度".format([kp_tips[related_points[i]] for i in [0, 1, 3]])
        elif key == 'distance':
            for point_key in standard_data[key]:
                tmp = point_key.split('-')
                # bg_point = int(tmp[0])  # 某个关节点
                bg_point = key_point[int(tmp[0])][0]  # 该点的x,y值的list
                bg_point.append(int(tmp[0]))
                # target_point = int(tmp[1])
                target_point = key_point[int(tmp[1])][0]
                target_point.append(int(tmp[1]))
                type1 = tmp[-1]
                # target_point & bg_point放的是该点的x,y值的list
                words = cal_if_located(target_point, bg_point, type1, standard_data[key][point_key])
                return words
