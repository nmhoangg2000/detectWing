import numpy as np
import cv2

def readtps(input):

   
    tps_file = open(input, 'r')  
    tps = tps_file.read().splitlines()  
    tps_file.close()

    lm, im, ID, coords_array = [], [], [], []

    for i, ln in enumerate(tps):
        if ln.startswith("LM"):
            lm_num = int(ln.split('=')[1])
            lm.append(lm_num)
            coords_mat = []
            
            for j in range(i + 1, i + 1 + lm_num):
                coords_mat.append(tps[j].split(' ')) 

            coords_mat = np.array(coords_mat, dtype=float)
            coords_array.append(coords_mat)
           
        if ln.startswith("IMAGE"):
            im.append(ln.split('=')[1])

        if ln.startswith("ID"):
            ID.append(ln.split('=')[1])

    all_lm_same = all(x == lm[0] for x in lm)
    
    if all_lm_same:
        coords_array = np.dstack(coords_array)

    return {'lm': lm, 'im': im, 'id': ID, 'coords': coords_array}

def check(xmin, ymin, xmax, ymax):
    if((xmax-xmin+1<20)or(ymax-ymin+1<20)): 
        return 0
    if((xmin>xmax) or(ymin>ymax)):
        return 0
    return 1


import os 
import xml.etree.cElementTree as ET
for file in os.listdir('./RightWings'):
    if(file[-3:]=="tps"):
        link = os.path.join("./RightWings", file)
        tps1 = readtps(link)
        imagename = file[:-4]+".jpg"
        img = cv2.imread("./data/"+imagename)
        
        root = ET.Element("annotation")
        folder = ET.SubElement(root, "folder").text = "images"
        filename = ET.SubElement(root,"filename").text =imagename
        path = ET.SubElement(root,"path").text = "/home/anhnh/dataset/data/"+imagename
        source = ET.SubElement(root,"source")

        ET.SubElement(source, "database").text = "unknowned"
        size = ET.SubElement(root, "size")
        ET.SubElement(size, "width").text = str(int(1024))
        ET.SubElement(size, "height").text = str(int(1360))
        ET.SubElement(size, "depth").text = str(int(3))
        segment = ET.SubElement(root, "segment").text = str(int(0))
        
        objectt = []
        cou = 0
        
        for i in range(15):
            firstcoord = tps1['coords'][i][0][0]
            secondcoord = tps1['coords'][i][1][0]

            secondcoord = img.shape[0] - secondcoord

            if(firstcoord>=15):
                xmin = int(firstcoord-15)
            else:
                xmin = int(0)
            if(secondcoord>=15):
                ymin = int(secondcoord-15)
            else :
                ymin = int(0)
            if(firstcoord+15<1024):
                xmax = int(firstcoord+15)
            else:
                xmax = int(1023)
            if(secondcoord+15<1360):
                ymax = int(secondcoord+15)
            else:
                ymax = int(1359)
            
            if(check(xmin,ymin,xmax,ymax)==1):
                objectt.append(ET.SubElement(root, "object"))
                ET.SubElement(objectt[cou], "name").text = str(cou)
                ET.SubElement(objectt[cou], "pose").text = "Unspecified"
                ET.SubElement(objectt[cou], "truncated").text = str(int(0))
                ET.SubElement(objectt[cou], "difficult").text = str(int(0))    
                bndbox = ET.SubElement(objectt[cou], "bndbox")
                ET.SubElement(bndbox, "xmin").text = str(xmin)
                ET.SubElement(bndbox, "ymin").text = str(ymin)
                ET.SubElement(bndbox, "xmax").text = str(xmax)
                ET.SubElement(bndbox, "ymax").text = str(ymax)
                cou=cou+1;
        tree = ET.ElementTree(root)
        tree.write("./data/"+file[:-4]+".xml")

