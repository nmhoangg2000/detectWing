import cv2
import os

for file in os.listdir("/home/hoangnm/dataset2/image1"):
    link = os.path.join("/home/hoangnm/dataset2/image1", file)
    tmp = cv2.imread(link)
    cv2.imwrite("/home/hoangnm/dataset2/data/"+file[:-4]+".jpg", tmp)
