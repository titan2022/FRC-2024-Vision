import math
import cv2 as cv
import numpy as np

def transformation_matrix():
	print()

def hsv_filter(color_matrix: np.ndarray, hsv_threshold: list) -> np.ndarray:
	return cv.inRange(color_matrix, np.array([hsv_threshold[0], hsv_threshold[2], hsv_threshold[4]]), np.array([hsv_threshold[1], hsv_threshold[3], hsv_threshold[5]]))

def get_position(position_matrix: np.ndarray, binary_mask: np.ndarray) -> np.ndarray:
	return cv.mean(position_matrix, binary_mask)

