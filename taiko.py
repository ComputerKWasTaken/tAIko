from PIL import Image
import numpy as np
from mss import mss
import keyboard

# Constants for screen area to capture
MONITOR = {"top": 415, "left": 705, "width": 98, "height": 111}

# Key bindings
KEY_RED = 'f'
KEY_BLUE = 'd'

# Color thresholds for detection using Pillow
COLOR_RED_RANGE = ((10, 25, 90), (20, 35, 100))
COLOR_BLUE_RANGE = ((70, 70, 35), (80, 80, 45))
COLOR_YELLOW_RANGE = ((0, 71, 95), (10, 81, 105))

def detect_color_and_act(image, color_range, key):
    image_np = np.array(image)
    mask = cv2.inRange(image_np, *color_range)
    if np.count_nonzero(mask) > 0:
        keyboard.press(key)
        keyboard.release(key)
        return True
    return False

def screen_record():
    with mss() as sct:
        while True:
            image = Image.frombytes('RGB', (sct.monitors[0]['width'], sct.monitors[0]['height']), sct.shot(output='bytes'))
            screen = image.crop((MONITOR['left'], MONITOR['top'], MONITOR['left'] + MONITOR['width'], MONITOR['top'] + MONITOR['height']))

            if detect_color_and_act(screen, COLOR_RED_RANGE, KEY_RED):
                continue
            if detect_color_and_act(screen, COLOR_BLUE_RANGE, KEY_BLUE):
                continue

            while detect_color_and_act(screen, COLOR_YELLOW_RANGE, KEY_RED):
                detect_color_and_act(screen, COLOR_YELLOW_RANGE, KEY_BLUE)
                screen = Image.frombytes('RGB', (sct.monitors[0]['width'], sct.monitors[0]['height']), sct.shot(output='bytes')).crop((MONITOR['left'], MONITOR['top'], MONITOR['left'] + MONITOR['width'], MONITOR['top'] + MONITOR['height']))

if __name__ == "__main__":
    screen_record()