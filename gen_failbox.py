# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import cv2

fa = open('./fail.txt','r')
for lines in fa:
    lines=lines.replace('[','')
    lines=lines.replace(']','')
    lines=lines.replace(',','')
    line = lines.split()
    path = line[0]   
    num = line[1]
    #seq = []
    for i in range(int(num)):
        #line[i+2] = line[i+2]
        ll = len(line[i+2])
        lall = '/img0000001'
        lnew = lall[0:11-ll]
        
        origin_pic = cv2.imread('./VisDrone2019-SOT-train_part2/VisDrone2018-SOT-train/sequences/' 
                                + path + lnew + line[i+2] +'.jpg')
        with open('./VisDrone2019-SOT-train_part2/VisDrone2018-SOT-train/annotations/'+ path + '.txt', 'r') as f:
                 lines1 = f.readlines()
                 count = int(line[i+2])
                 lines1 = str(lines1[count-1])
                 line1 = lines1.split(',')
                 x = int(line1[0])
                 y = int(line1[1])
                 w = int(line1[2])
                 h = int(line1[3])
                 pic = cv2.rectangle(origin_pic, (x, y), (x+w, y+h), (255, 0, 0), 2)
                 #cv2.imshow("image",pic)
                 #cv2.waitKey(10)
                 dirs = './gen_box/'+ path 
                 if not os.path.exists(dirs):
                       os.makedirs(dirs)
                 cv2.imwrite(dirs + lnew + line[i+2] +'.jpg', pic)


