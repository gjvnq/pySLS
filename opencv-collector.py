#!/usr/bin/env python3

import os
import sys
from pathlib import Path
import numpy as np
import cv2 as cv
import imutils
import time

def current_milli_time():
    return round(time.time() * 1000)

def show_webcam():
	cap = cv.VideoCapture(0)
	if not cap.isOpened():
		print("Cannot open camera")
		exit()
	print(cap.getBackendName())
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
		gray = frame
		# Display the resulting frame
		cv.imshow('webcam-preview', gray)
		if cv.waitKey(1) == 27: #ESC
			break
	# When everything done, release the capture
	cap.release()
	cv.destroyWindow('webcam-preview')


# Don't go above level 10
def make_vertical_binary_stripes(level, width, height):
	size = (height, width, 3)
	img = np.zeros(size, np.uint8)
	n_cols = 2**level
	col_width = int(width/n_cols)
	if col_width == 0:
		print(f"Error: lines too small for width={width} and level={level}")
		return None
	
	n_cols = int(width/col_width+1)
	for i in range(n_cols):
		col_start = i*col_width
		col_end = min(width, col_start+col_width)
		if i % 2 == 1:
			img[:,col_start:col_end,:] = 255
		else:
			img[:,col_start:col_end,:] = 0

	return img

def make_horizontal_binary_stripes(level, width, height):
	img = make_vertical_binary_stripes(level, height, width)
	if img is not None:
		return np.rot90(img)
	else:
		return None

class Collector:
	webcam: cv.VideoCapture
	output_dir: Path

	def __init__(self, webcam: cv.VideoCapture, output_dir: str):
		if not webcam.isOpened():
			raise ValueError("Cannot open camera")
		
		self.webcam = webcam
		self.capture_mode = None
		self.output_dir = Path(output_dir)
		if self.output_dir.exists() and (not self.output_dir.is_dir()):
			raise ValueError(f"path {output_dir} is not a directory")
		elif not self.output_dir.exists():
			self.output_dir.mkdir(parents=True)

		self._make_patterns()

	def _make_patterns(self):
		self.patterns = []
		self.current_pattern = 0

		# I should latter change it to match the projector
		width = int(self.webcam.get(cv.CAP_PROP_FRAME_WIDTH))
		height = int(self.webcam.get(cv.CAP_PROP_FRAME_HEIGHT))

		name = 'black'
		pat = np.zeros((height, width, 3), np.uint8)
		self.patterns.append((name, pat, 'color'))

		name = 'white'
		pat = np.zeros((height, width, 3), np.uint8)
		pat[:,:,:] = 255
		self.patterns.append((name, pat, 'color'))

		for level in range(12):
			name = f'vert-L{level:02}-{width:04}x{height:04}'
			pat = make_vertical_binary_stripes(level, width, height)
			if pat is not None:
				self.patterns.append((name, pat, 'gray'))

			name = f'horz-L{level:02}-{width:04}x{height:04}'
			pat = make_horizontal_binary_stripes(level, width, height)
			if pat is not None:
				self.patterns.append((name, pat, 'gray'))

	def _get_webcam(self):
		# Capture frame-by-frame
		ret, self.cam_color = self.webcam.read()
		# if frame is read correctly ret is True
		if not ret:
			raise ValueError("Can't receive frame (stream end?). Exiting ...")
		# Our operations on the frame come here
		self.cam_gray = cv.cvtColor(self.cam_color, cv.COLOR_BGR2GRAY)

	def _step_preview(self):
		self._get_webcam()
		patname, pat, patmode = self.patterns[self.current_pattern]
		if patmode == 'color':
			minicam = imutils.resize(self.cam_color, width=320)
		else:
			minicam = imutils.resize(self.cam_gray, width=320)
			minicam = np.stack((minicam,)*3, axis=-1)
		minipat = imutils.resize(pat, width=320)
		self.imggui =np.concatenate((minicam, minipat), axis=1)

	def _start_capture(self):
		self.current_pattern = 0
		self.capture_start_time = current_milli_time()
		self.capture_mode = 'project'

	def _stop_capture(self):
		self.current_pattern = 0
		self.capture_start_time = None
		self.capture_mode = None

	def _step_capture(self):
		if self.capture_mode is None:
			return

		patname, pat, patmode = self.patterns[self.current_pattern]

		if self.capture_mode is 'project':
			cv.imshow('projector', pat)
			self.capture_wait_until = current_milli_time()+500
			self.capture_mode = 'project-wait'
		if self.capture_mode is 'project-wait':
			if current_milli_time() >= self.capture_wait_until:
				self._get_webcam()
				filename = f"{self.capture_start_time}_{self.current_pattern:02}_{patname}.png"
				if patmode == 'color':
					webcam = self.cam_color
				else:
					webcam = self.cam_gray
				filename = str(self.output_dir.joinpath(filename))
				cv.imwrite(filename, webcam)

				self.current_pattern += 1
				if self.current_pattern >= len(self.patterns):
					self._stop_capture()
				else:
					self.capture_mode = 'project'

	def loop(self):
		while True:
			self._step_preview()
			self._step_capture()
			cv.imshow('imggui', self.imggui)
			key = cv.waitKey(250)
			if key == 27: #ESC
				break
			if key == ord('c'): #ESC
				print("Starting capture")
				self._start_capture()

	def __del__(self):
		self.webcam.release()
		cv.destroyAllWindows()

def main():
	if len(sys.argv) != 3:
		print(f"USAGE: {sys.argv[0]} [CAMERA PATH OR NUM] [OUTPUT_DIR]")
		exit()

	try:
		webcam = cv.VideoCapture(int(sys.argv[1]))
	except:
		webcam = cv.VideoCapture(sys.argv[1])
	app = Collector(webcam, sys.argv[2])
	app.loop()

if __name__ == "__main__":
	main()
