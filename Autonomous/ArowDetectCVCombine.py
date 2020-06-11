from __future__ import print_function
import cv2
import numpy as np
import argparse
import random as rng

rng.seed(12345)


def get_contour_areas(contours):
    all_areas = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        all_areas.append(area)
    return np.max(all_areas)


def drawContours11111(img):
    blur = cv2.medianBlur(img, 5)
    edged = cv2.Canny(blur,240, 255)
    contours, heirarchy = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    blank_image = np.zeros([img.shape[0], img.shape[1], 3], dtype=np.uint8)
    blank_image.fill(255)
    maxarea = get_contour_areas(contours)
    return blank_image,maxarea


def thresh_callback(val):
    threshold = val

    ret,th = cv2.threshold(src_gray,127,255,cv2.THRESH_BINARY)
    canny_output = cv2.Canny(th, threshold, 255)
    contours, _ = cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    color = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
    areas = [cv2.contourArea(c) for c in contours]
    max_index = np.argmax(areas)
    area = cv2.contourArea(contours[max_index])

    if area > 50000:
        print("Area is too near to object")
        cnt = contours[max_index]
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(src, (x, y), (x + w, y + h),color, 2)
        cv2.circle(src,(x+int(w/2),y+int(h/2)),3,color,-1)
        cropped_image = src[y:y+h,x:x+w]
        predict_again(cropped_image)

    if area > 1000:
        cnt = contours[max_index]
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(src, (x, y), (x + w, y + h),color, 2)
        cv2.circle(src,(x+int(w/2),y+int(h/2)),3,color,-1)
        cropped_image = src[y:y+h,x:x+w]
        predict_again(cropped_image)

    cv2.imshow("source_window", src)



def predict_again(src):
    H,W = src.shape[:2]

    img1 = src[:,:int(W/2)]
    img2 = src[:,int(W/2)+1:]
    contoured1,area1 = drawContours11111(img1)
    contoured2,area2 = drawContours11111(img2)

    if area2>area1:
        print ("New:::::::::::::RIGGGGGGGGGHT")
    elif area1>area2:
        print ("New:::::::::::::LEFTTTTTTTTT")


cap= cv2.VideoCapture(0)

while True:
    _,frame = cap.read()
    img = frame.copy()
    src = frame.copy()
    src_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    src_gray = cv2.blur(src_gray, (3, 3))
    thresh = 100
    try:
        thresh_callback(thresh)
    except ValueError:
        pass
    cv2.imshow("source_window", src)
    if cv2.waitKey(1)==13:
        break

cap.release()
cv2.destroyAllWindows()