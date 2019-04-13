#!/usr/bin/python3

from darknet import performDetect
from collections import Counter


with open("data/test.txt") as f:
    data = f.readlines()
data = [x.strip() for x in data] 

right = 0
wrong = 0

for image in data:
	res = performDetect(
		imagePath = image, 
		configPath = "yolov3-414.cfg", 
		metaPath= "data/414.data",
		weightPath = "backup/yolov3-414_final.weights",
		showImage = False)
	
	cnt = Counter([x[0] for x in res])
	detections = sorted(list(cnt.items()), key=lambda x: x[1], reverse=True)
	classification = '';
	if len(detections) > 0 and detections[0][1] >= 32:
		classification = detections[0][0]		
		
	print('class:', classification)
	
	# verify
	actual_class = ''
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

print('right:', right, 'wrong:', wrong, "percent right: %.3f%"%(100*right/(right+wrong)))







