# 必须使用 python3以上版本

# 鼠标画出多个目标框进行跟踪(每画一个，点击一下enter键)


import numpy as np
import cv2
import sys
import time


# 打开摄像头，读取第一帧图像
cv2.namedWindow("tracking")
camera = cv2.VideoCapture("videos/exam_small.mp4")
ok_cam, image_pre = camera.read()
if not ok_cam:
    print('Failed to read video')
    exit()

img_h, img_w, c = image_pre.shape
image = cv2.resize(image_pre, (int(img_w/2), int(img_h/2)))

# 初始化num_obj个目标
num_obj = 20
bbox_list = []
tracker_list = []

for i in range(0, num_obj):
    bbox_tmp = cv2.selectROI('tracking', image)
    bbox_list.append(bbox_tmp)

    tracker_tmp = cv2.TrackerMOSSE_create()
    ok_tmp = tracker_tmp.init(image, bbox_tmp)
    tracker_list.append(tracker_tmp)


# 循环处理
while camera.isOpened():

    ok_cam, image_pre = camera.read()

    if not ok_cam:
        print ('no image to read')
        break

    img_h, img_w, c = image_pre.shape
    image = cv2.resize(image_pre, (int(img_w / 2), int(img_h / 2)))

    bbox_info = []

    # 更新跟踪结果
    pre = time.time()
    for tracker in tracker_list:
        ok_t, bbox_t = tracker.update(image)
        bbox_info.append((ok_t, bbox_t))
    print(time.time() - pre, '*********')

    # 在图像上显示跟踪结果
    for tmp_info in bbox_info:
        newbox = tmp_info[1]
        p1 = (int(newbox[0]), int(newbox[1]))
        p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
        cv2.rectangle(image, p1, p2, (200,0,0))

    cv2.imshow('tracking', image)
    k = cv2.waitKey(1)
    if k == 27 : break # esc pressed
