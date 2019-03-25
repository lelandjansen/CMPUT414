import cv2

img = cv2.imread('20190324232701.png')

for line in open('20190324232701.txt'):
	obj, x_center, y_center, width, height = map(float, line.split(" "))
	cv2.rectangle(img, 
			(int(x_center-width/2.0), int(y_center-height/2.0)), 
			(int(x_center+width/2.0), int(y_center+height/2.0)), 
			(255,0,0), 2)

cv2.imshow("lalala", img)
k = cv2.waitKey(0) # 0==wait forever

