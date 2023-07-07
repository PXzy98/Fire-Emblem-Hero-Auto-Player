# from datetime import time
# from typing import List, Tuple
#
# import cv2
# import numpy as np
# import pyautogui
#
#
# def non_max_suppression_fast(boxes: List[Tuple[int, int]], overlapThresh: float, template) -> List[Tuple[int, int]]:
#     # If there are no boxes, return an empty list
#     if len(boxes) == 0:
#         return []
#
#     pick = []
#
#     # Grab the coordinates of the bounding boxes
#     x1 = [b[0] for b in boxes]
#     y1 = [b[1] for b in boxes]
#     x2 = [b[0] + template.shape[1] for b in boxes]  # Assuming the width of the box is the same as the template's
#     y2 = [b[1] + template.shape[0] for b in boxes]  # Assuming the height of the box is the same as the template's
#
#     # Compute the area of the bounding boxes and sort the bounding
#     # boxes by the bottom-right y-coordinate of the bounding box
#     area = (np.array(x2) - np.array(x1) + 1) * (np.array(y2) - np.array(y1) + 1)
#     idxs = np.argsort(y2)
#
#     # Keep looping while some indexes still remain in the indexes list
#     while len(idxs) > 0:
#         # Grab the last index in the indexes list and add the index value to the list of picked indexes
#         last = len(idxs) - 1
#         i = idxs[last]
#         pick.append(boxes[i])
#
#         # Find the largest (x, y) coordinates for the start of the bounding box and the smallest (x, y) coordinates for the end of the bounding box
#         xx1 = np.maximum(x1[i], np.array(x1)[idxs[:last]])
#         yy1 = np.maximum(y1[i], np.array(y1)[idxs[:last]])
#         xx2 = np.minimum(x2[i], np.array(x2)[idxs[:last]])
#         yy2 = np.minimum(y2[i], np.array(y2)[idxs[:last]])
#
#         # Compute the width and height of the bounding box
#         w = np.maximum(0, xx2 - xx1 + 1)
#         h = np.maximum(0, yy2 - yy1 + 1)
#
#         # Compute the ratio of overlap
#         overlap = (w * h) / area[idxs[:last]]
#
#         # Delete all indexes from the index list that have overlap greater than the provided overlap threshold
#         idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > overlapThresh)[0])))
#
#     # Return only the bounding boxes that were picked
#     return pick
#
# def count_color(color):
#     template_path = "pics/loot/colors/"+color+".png"
#
#     # Read the template in color
#     template = cv2.imread(template_path)
#
#     # Take a screenshot of the screen
#     screenshot = pyautogui.screenshot()
#
#     # Convert the PIL Image to an OpenCV (BGR) image
#     screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
#
#     # Perform template matching
#     result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
#
#     # Set a threshold to determine matches
#     threshold = 0.8
#     locations = np.where(result >= threshold)
#     # matches = zip(*locations[::-1])
#     matches = list(zip(*locations[::-1]))
#     matches = non_max_suppression_fast(matches, 0.5, template)
#     # Return the count of unique matches
#     return len(matches)
# def check_image_similar(template_path):
#     template = cv2.imread(template_path, 0)
#
#     # Take a screenshot of the screen
#     screenshot = pyautogui.screenshot()
#     screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
#
#     # Perform template matching
#     result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
#
#     # Set a threshold to determine matches
#     threshold = 0.7
#     locations = np.where(result >= threshold)
#     matches = zip(*locations[::-1])
#
#     # Iterate over the matches
#     for match in matches:
#         icon_x, icon_y = match
#         return icon_x, icon_y
#
# def action_passer(path):
#     unchanged = path
#     path_replaced = unchanged.replace("pics/loot/", "")
#     path_replaced = path_replaced.replace(".png", "")
#     print(path_replaced, end=" ")
#     icon_x, icon_y = None, None
#     for i in range(10):
#         time.sleep(0.1)
#         try:
#             icon_x, icon_y = check_image_similar(path)
#         except Exception as e:
#             print("*", end="")
#         if icon_y is not None:
#             pyautogui.moveTo(icon_x + 40, icon_y + 20)
#             pyautogui.click()
#             print("完成")
#             return True
#
#     print(" 未发现")
#     return False
#
# action_passer()
import os
from datetime import datetime

import numpy as np
import pygetwindow as gw
import pyautogui
import time


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def take_partial_screenshots(window, directory, num_screenshots, partial_coords, filename):
    # Get the coordinates of the window and add the partial coordinates
    x = window.left + partial_coords[0]
    y = window.top + partial_coords[1]
    width = partial_coords[2]
    height = partial_coords[3]

    # Ensure the directory exists
    ensure_dir(directory)

    for i in range(num_screenshots):
        # Capture a screenshot of the region
        screenshot = pyautogui.screenshot(region=(x, y, width, height))

        # Create a timestamp string for the filename
        # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        timestamp = filename

        # Save the screenshot to a file
        screenshot.save(os.path.join(directory, filename + "_" + str(i) + '.png'))

        # Wait for the next interval (0.1 seconds for 10 times per second)
        time.sleep(0.1)


# Usage
# window = gw.getWindowsWithTitle('模拟器')[0]
#
#
#         # Activate the window
# window.activate()
#
# pos1 = (205, 215, 130, 130)
# pos2 = (50, 330, 130, 130)
# pos3 = (110, 513, 130, 130)
# pos4 = (305, 513, 130, 130)
# pos5 = (360, 330, 130, 130)
#
# # Modify this to specify the area you want to capture
# # partial_coords = (205, 212, 125, 125)
#
# take_partial_screenshots(window, "C:\\Users\\xzy19\\Desktop\\1\\", 3, pos1,"pos1_")
# take_partial_screenshots(window, "C:\\Users\\xzy19\\Desktop\\1\\", 3, pos2,"pos2_")
# take_partial_screenshots(window, "C:\\Users\\xzy19\\Desktop\\1\\", 3, pos3,"pos3_")
# take_partial_screenshots(window, "C:\\Users\\xzy19\\Desktop\\1\\", 3, pos4,"pos4_")
# take_partial_screenshots(window, "C:\\Users\\xzy19\\Desktop\\1\\", 3, pos5,"pos5_")
#
# Green     12345
# Red       12345
# Blue      12345
# White     12345

# hide:
# Green     12345
# Red       12345
# Blue      12345
# White     12345

# take_partial_screenshots(window, "C:\\Users\\xzy19\\Desktop\\1\\", 10, partial_coords)
#
# while True:
#     input("Press Enter to get mouse position:")
#     print(pyautogui.position())
import math
import pyautogui

x, y, width, height = 0, 0, 0, 0
try:
    window = gw.getWindowsWithTitle('模拟器')[0]

    # Activate the window
    window.activate()

    x, y, width, height = window.left, window.top, window.width, window.height

except Exception as e:
    x, y, width, height = 0, 0, 900, 600

x_range = round(width / 3,-2)
y_range = round(height / 3,-2)

print(-(x_range))