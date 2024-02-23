import math
import cv2
import numpy as np

def transformation_matrix():
	print()

def hsv_filter(color_matrix, hsv_threshold, output_matrix):
	cv2.inRange(color_matrix, cv2.Scalar(hsv_threshold[0], hsv_threshold[2], hsv_threshold[4]), cv2.Scalar(hsv_threshold[1], hsv_threshold[3], hsv_threshold[5]), output_matrix)

def get_position(position_matrix, binary_mask):
	return cv2.mean(position_matrix, binary_mask)

