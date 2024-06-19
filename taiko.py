import cv2
import numpy as np
from mss import mss
from pynput.keyboard import Controller, Key
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants for screen area to capture
MONITOR = {"top": 415, "left": 705, "width": 98, "height": 111}

# Key bindings
KEY_RED = 'f'
KEY_BLUE = 'd'

# Color thresholds for detection using OpenCV
COLOR_RED_RANGE = ((10, 25, 90), (20, 35, 100))
COLOR_BLUE_RANGE = ((70, 70, 35), (80, 80, 45))
COLOR_YELLOW_RANGE = ((0, 71, 95), (10, 81, 105))

# Initialize keyboard controller
keyboard = Controller()

def detect_color_and_act(image, color_range, key):
    mask = cv2.inRange(image, np.array(color_range[0]), np.array(color_range[1]))
    if np.count_nonzero(mask) > 0:
        logging.info(f"Detected color for key {key}")
        keyboard.press(key)
        keyboard.release(key)
        return True
    return False

def screen_record():
    with mss() as sct:
        while True:
            sct_img = sct.grab(MONITOR)
            img = np.array(sct_img)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            
            if detect_color_and_act(img_rgb, COLOR_RED_RANGE, KEY_RED):
                continue
            if detect_color_and_act(img_rgb, COLOR_BLUE_RANGE, KEY_BLUE):
                continue

            while detect_color_and_act(img_rgb, COLOR_YELLOW_RANGE, KEY_RED):
                detect_color_and_act(img_rgb, COLOR_YELLOW_RANGE, KEY_BLUE)
                sct_img = sct.grab(MONITOR)
                img = np.array(sct_img)
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

if __name__ == "__main__":
    screen_record()
