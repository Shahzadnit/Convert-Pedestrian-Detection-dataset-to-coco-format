import cv2
import numpy as np
import glob
import json

files = glob.glob("Annotation_train/*.txt")

# print(files)

def extract_coor(line):
    xmin,ymin = int((line.split(":")[-1]).split('-')[0].split(',')[0][2:]),int((line.split(":")[-1]).split('-')[0].split(',')[1][:-2])
    # print(int((lines[10].split(":")[-1]).split('-')[1].split(',')[0][2:]),int((lines[10].split(":")[-1]).split('-')[1].split(',')[1][:-2]))
    xmax,ymax = int((line.split(":")[-1]).split('-')[1].split(',')[0][2:]),int((line.split(":")[-1]).split('-')[1].split(',')[1][:-2])
    return xmin,ymin,xmax,ymax

res = []
for file in files:
    print('#############################################')
    objs = []
    with open(file, 'r') as f:
        lines = f.readlines()
        image_name = lines[1].split(":")[-1].split('/')[-1][:-2]
        image = cv2.imread('PNGImages/'+image_name)
        # mask_name = image_name.split('.')[0]+'_mask.png'
        # mask = cv2.imread('PedMasks/'+mask_name)
        cv2.imwrite('mask/'+image_name,mask)
        # print(mask.shape)
        # print(lines)
        for line in lines:
            # print(line)
            if 'Bounding box' in line:
                print(line)
                xmin,ymin,xmax,ymax = extract_coor(line)
                bbox = [xmin,ymin,xmax,ymin,xmax,ymax,xmin,ymax]
                text = 'human'
                bbox = [int(coord) for coord in bbox]
                anno = {'category_id': 1, 'bbox': bbox, 'text': text,'isDifficult': 1 if text=='###' else 0}
                objs.append(anno)

                start_point = (xmin,ymin)
                end_point = (xmax,ymax)
                image = cv2.rectangle(image, start_point, end_point, (255, 0, 0), 2)
        
        print(image_name)

        # cv2.imwrite('temp/'+image_name,image)
        
    anno = {'img_name': image_name,'height': image.shape[0],'width': image.shape[1],'objs': objs}
    res.append(anno)   

with open('annotations_train.json', 'w') as f:
    json.dump(res, f) 






