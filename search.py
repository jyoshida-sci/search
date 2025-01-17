import numpy as np
import cv2
import random
import os
import sys
import glob
import pathlib
import pickle
import matplotlib.pyplot as plt
import csv

def binarize (img):
    img_blur = cv2.GaussianBlur(img,(31,31),0,0)
    img_sub = cv2.subtract(img_blur,img)
    _, binary = cv2.threshold(img_sub,15,255,cv2.THRESH_BINARY)
    return binary

def change_imgsize(img):
    height = img.shape[0]
    width = img.shape[1]
    ratio = 0.29/0.15
    resized_img = cv2.resize(img , (int(width*ratio), int(height*ratio)))
    return resized_img

def template_match(img,temp):
    w, h = temp.shape[::-1]
    result = cv2.matchTemplate(img, temp, cv2.TM_CCORR_NORMED)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
    top_left = maxLoc
    btm_right = (top_left[0] + w, top_left[1] + h)
    return maxVal,top_left,btm_right





filename = 'img_search'
imgs = glob.glob(filename + "/*.png")
imgs.sort()
img_ori = cv2.imread('img_ori.png', 0)

f = open('search.csv', 'w')
writer = csv.writer(f, lineterminator='\n')
writer.writerow(['i','max_value', 'top_left','btm_right'])

list_result = []

list_maxvalue = []
mv = 0
if __name__ == "__main__":
    
    for i in range(len(imgs)):
        img = cv2.imread(imgs[i], 0)
        niti = binarize(img)
        niti_ori = binarize(img_ori)
        
        resized_niti_ori = change_imgsize(niti_ori)

        maxVal , top_left,btm_right = template_match(niti,resized_niti_ori)
        
        result = {}
        result["id"] = i
        result["maxVal"] = maxVal
        result["top_left"] = top_left
        result["btm_right"] = btm_right
        list_maxvalue.append(maxVal)
        list_result.append(result)
        writer.writerow([i,maxVal,top_left,btm_right]) 
        print(i)
        
    f.close
   
    
    
    '''    
    cv2.rectangle(img_use,tl, br, 255, 2)
    cv2.imshow(str(i_use),img_use)
    cv2.waitKey(0)    
    '''

    #with open('search.pickle', 'wb') as f:
        #pickle.dump(list_result, f)
