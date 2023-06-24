import time

import cv2
import pyautogui
import numpy as np
import tkinter as tk
import os

def show_completion_window(x, y):
    # Create a new window
    window = tk.Toplevel()
    window.title("Process Completed")

    # Set the window size and position
    window.geometry("200x200+{}+{}".format(x, y))

    # Create a canvas to display the circle
    canvas = tk.Canvas(window, width=150, height=150)
    canvas.pack()

    # Draw a circle on the canvas
    canvas.create_oval(25, 25, 125, 125, fill="green")

    # Run the main event loop
    window.mainloop()

def check_image(folder_path):
    matches = []  # List to store the matching results

    # Take a screenshot of the screen
    screenshot = pyautogui.screenshot()
    screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    # Iterate over the files in the folder
    for filename in os.listdir(folder_path):
        # Filter the files based on file extension (e.g., .png, .jpg)
        if filename.endswith('.png') or filename.endswith('.jpg'):
            # Construct the template image path
            template_path = os.path.join(folder_path, filename)

            # Load the template image
            template = cv2.imread(template_path, 0)

            # Perform template matching
            result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)

            # Set a threshold to determine matches
            threshold = 0.8
            locations = np.where(result >= threshold)
            template_matches = zip(*locations[::-1])

            # Add the matches to the list
            matches.extend(template_matches)

    # Iterate over the matches
    for match in matches:
        icon_x, icon_y = match
        return icon_x, icon_y

icon_x, icon_y  = check_image("pics/second_level")




pyautogui.moveTo(icon_x+150, icon_y+30)
time.sleep(3)
pyautogui.moveTo(icon_x, icon_y)
pyautogui.click()



