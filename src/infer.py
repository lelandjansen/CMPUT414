#!/usr/bin/python3

from darknet import performDetect
from collections import Counter
from sklearn.metrics import precision_recall_fscore_support, classification_report
import time

VOTING_THRESHOLD = 58
DEBUG = False


# find the test images
with open("data/test.txt") as f:
    data = f.readlines()
data = [x.strip() for x in data] 


# count the number of right and wrong classifications and
# also record our ground truth and infered classes so that
# we can perform analysis on the data later.
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
    if len(detections) > 0 and detections[0][1] >= VOTING_THRESHOLD:
            classification = detections[0][0]		

    if DEBUG: print('class:', classification)

    # verify whether the class is correct
    actual_class = 'none'
    labels = ".".join(image.split('.')[:-1])+".txt"
    with open(labels) as f:
            boxes = f.readlines()
    if len(boxes) > 0:
            class_id = int(boxes[0].split(' ')[0])
            if class_id == 0: actual_class = 'car'
            else: actual_class = 'pedestrian'

    if actual_class != classification:
            if DEBUG: print("wrong!!!!!!!!!!!!!!!!", image, detections[0][1], actual_class)
            wrong += 1
    else:
            right += 1
    
    y_true.append(actual_class)
    y_pred.append(classification)

accuracy = (100*right/(right+wrong))
print("t_avg = {}ms".format(time.time()-t0))
print('right:', right, 'wrong:', wrong, "accuracy: %.3f%%" % accuracy)
print(classification_report(y_true, y_pred, target_names=['car', 'pedestrian', 'none'], digits=4))


