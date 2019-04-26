#!/usr/bin/python3

from darknet import performDetect
from collections import Counter
from sklearn.metrics import precision_recall_fscore_support, classification_report
import time

with open("data/test.txt") as f:
    data = f.readlines()
data = [x.strip() for x in data] 


threshold = 58

right = 0
wrong = 0

y_true = []
y_pred = []
t0 = time.time()

for image in data:
    res = performDetect(
            imagePath = image, 
            configPath = "data/yolov3-414.cfg", 
            metaPath= "data/414.data",
            weightPath = "yolov3-414_final.weights",
            showImage = False)

    cnt = Counter([x[0] for x in res])
    detections = sorted(list(cnt.items()), key=lambda x: x[1], reverse=True)
    classification = 'none';
    if len(detections) > 0 and detections[0][1] >= threshold:
            classification = detections[0][0]		

    print('class:', classification)

    # verify
    actual_class = 'none'
    labels = ".".join(image.split('.')[:-1])+".txt"
    with open(labels) as f:
            boxes = f.readlines()
    if len(boxes) > 0:
            class_id = int(boxes[0].split(' ')[0])
            if class_id == 0: actual_class = 'car'
            else: actual_class = 'pedestrian'

    if actual_class != classification:
            print("wrong!!!!!!!!!!!!!!!!", image, detections[0][1], actual_class)
            wrong += 1
    else:
            right += 1
    
    y_true.append(actual_class)
    y_pred.append(classification)
                        
print("t_avg = {}ms".format(time.time()-t0))
percent = (100*right/(right+wrong))
print('right:', right, 'wrong:', wrong, "accuracy: %.3f%%" % percent)
print(classification_report(y_true, y_pred, target_names=['car', 'pedestrian', 'none'], digits=4))
