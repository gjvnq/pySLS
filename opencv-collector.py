#!/usr/bin/env python3

import numpy as np
import cv2 as cv

def show_webcam():
	cap = cv.VideoCapture(3)
	if not cap.isOpened():
		print("Cannot open camera")
		exit()
	cap.set(cv.CAP_PROP_FRAME_WIDTH,320)
	cap.set(cv.CAP_PROP_FRAME_HEIGHT,240)
	print("Press ESC to exit")
	while True:
		# Capture frame-by-frame
		ret, frame = cap.read()
		# if frame is read correctly ret is True
		if not ret:
			print("Can't receive frame (stream end?). Exiting ...")
			break
		# Our operations on the frame come here
		gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
		# Display the resulting frame
		cv.imshow('frame', gray)
		if cv.waitKey(1) == 27: #ESC
			break
	# When everything done, release the capture
	cap.release()
	cv.destroyAllWindows()


# Don't go above level 10
def make_vertical_binary_stripes(level, width=800, height=600):
	size = (height, width, 1)
	img = np.zeros(size, np.uint8)
	n_cols = 2**level
	col_width = int(width/n_cols)
	if col_width == 0:
		print(f"Warning: columns too small for width={width} and level={level}")
		return make_vertical_binary_stripes(level-1, width=width, height=height)
	
	n_cols = int(width/col_width+1)
	for i in range(n_cols):
		col_start = i*col_width
		col_end = min(width, col_start+col_width)
		if i % 2 == 1:
			img[:,col_start:col_end] = 255
		else:
			img[:,col_start:col_end] = 0

	return img

def make_horizontal_binary_stripes(level, width=800, height=600):
	img = make_vertical_binary_stripes(level, width=height, height=width)
	return np.rot90(img)

img = make_horizontal_binary_stripes(10, width=1920)
cv.imshow('result', img), cv.waitKey(0)
cv.destroyAllWindows()