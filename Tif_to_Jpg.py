import cv2
import os

for file in os.listdir("./RightWings"):
    if(file[-3:]=="tif"):
        link = os.path.join("./RightWings", file)
        tmp = cv2.imread(link)
        cv2.imwrite("./data/"+file[:-4]+".jpg", tmp)