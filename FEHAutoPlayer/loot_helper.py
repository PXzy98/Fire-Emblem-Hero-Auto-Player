import os
import sys
import pygetwindow as gw
import pyautogui
import time
import cv2
import pyautogui
import numpy as np
import tkinter as tk
import contextlib
from datetime import datetime


def take_screenshot(path, name, window_name):
    if not os.path.exists(path):
        os.makedirs(path)
    window = gw.getWindowsWithTitle(window_name)[0]

    # Activate the window
    window.activate()

    # Get the coordinates of the window
    x, y, width, height = window.left, window.top, window.width, window.height

    # Capture a screenshot of the region
    screenshot = pyautogui.screenshot(region=(x, y, width, height))

    # Save the screenshot to a file
    screenshot.save(path + name + ".png")


def check_image(folder_path):
    # matches = []
    # screenshot = pyautogui.screenshot()
    # screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    #
    # for filename in os.listdir(folder_path):
    #     if filename.endswith('.png') or filename.endswith('.jpg'):
    #         template_path = os.path.join(folder_path, filename)
    #         template = cv2.imread(template_path, 0)
    #         result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    #         threshold = 0.9
    #         locations = np.where(result >= threshold)
    #         template_matches = zip(*locations[::-1])
    #         matches.extend(template_matches)
    #
    # for match in matches:
    #     icon_x, icon_y = match
    #     return icon_x, icon_y
    matches = []

    # Take a screenshot of the screen
    screenshot = pyautogui.screenshot()

    # Convert the PIL Image to an OpenCV (BGR) image
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    for filename in os.listdir(folder_path):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            template_path = os.path.join(folder_path, filename)

            # Read the template in color
            template = cv2.imread(template_path)

            # Perform template matching
            result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)

            # Set a threshold to determine matches
            threshold = 0.9
            locations = np.where(result >= threshold)
            template_matches = zip(*locations[::-1])
            matches.extend(template_matches)
            if matches:
                for match in matches:
                    icon_x, icon_y = match
                    return icon_x, icon_y

    for match in matches:
        icon_x, icon_y = match
        return icon_x, icon_y


def check_image_similar_with_color(template_path):
    # Read the template in color
    template = cv2.imread(template_path)

    # Take a screenshot of the screen
    screenshot = pyautogui.screenshot()

    # Convert the PIL Image to an OpenCV (BGR) image
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Perform template matching
    result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)

    # Set a threshold to determine matches
    threshold = 0.7
    locations = np.where(result >= threshold)
    matches = zip(*locations[::-1])

    # Iterate over the matches
    for match in matches:
        icon_x, icon_y = match
        return icon_x, icon_y


def check_image_similar(template_path):
    template = cv2.imread(template_path, 0)

    # Take a screenshot of the screen
    screenshot = pyautogui.screenshot()
    screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    # Perform template matching
    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)

    # Set a threshold to determine matches
    threshold = 0.7
    locations = np.where(result >= threshold)
    matches = zip(*locations[::-1])

    # Iterate over the matches
    for match in matches:
        icon_x, icon_y = match
        return icon_x, icon_y


def action_passer(path):
    unchanged = path
    path_replaced = unchanged.replace("pics/loot/", "")
    path_replaced = path_replaced.replace(".png", "")
    print(path_replaced, end=" ")
    icon_x, icon_y = None, None
    for i in range(10):
        time.sleep(0.1)
        try:
            icon_x, icon_y = check_image_similar(path)
        except Exception as e:
            print("*", end="")
        if icon_y is not None:
            pyautogui.moveTo(icon_x + 40, icon_y + 20)
            pyautogui.click()
            print("完成")
            return True

    print(" 未发现")
    return False


def action_passer_no_reaction(path):
    icon_x, icon_y = None, None
    for i in range(10):
        time.sleep(0.1)
        try:
            icon_x, icon_y = check_image_similar(path)
        except Exception as e:
            print("", end="")
        if icon_y is not None:
            return True

    return False


def action_passer_with_color(path):
    print(path, end=" ")
    icon_x, icon_y = None, None
    for i in range(15):
        time.sleep(0.1)
        try:
            icon_x, icon_y = check_image_similar_with_color(path)
        except Exception as e:
            print("*", end="")
        if icon_y is not None:
            pyautogui.moveTo(icon_x + 40, icon_y + 20)
            pyautogui.click()
            print("完成")
            return True

    print(" 未发现")
    return False


def color_checker(color,c_fold):
    print("查询颜色 " + color + " : ", end="")
    icon_x, icon_y = None, None
    for i in range(5):
        time.sleep(0.1)
        try:
            icon_x, icon_y = check_image("pics/loot/"+c_fold+"/" + color + "_with_pos/")
        except Exception as e:
            print("*", end="")
        if icon_y is not None:
            pyautogui.moveTo(icon_x + 30, icon_y + 30)
            pyautogui.click()
            print("完成")
            return True

    print("未发现.")
    return False


def loot_processing(path1, input_colors, counting, window_name,version_fold):
    selected_colors = input_colors
    if not os.path.exists(path1 + "finished_wishes/"):
        os.makedirs(path1 + "finished_wishes/")
    current_time = datetime.now()

    # Format it as a string
    time_string = current_time.strftime("%Y-%m-%d-%H-%M-%S")
    screenshot_path = path1 + "finished_wishes/" + time_string + "/"
    round = 0
    i = 0
    take_screenshot(path1 + "finished_wishes/", time_string + "_" + str(round) + "_record_wish_pool", window_name)
    while i < counting:
        round = round + 1
        print("")
        print("iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
        time.sleep(2)
        if action_passer("pics/loot/free_summon.png"):
            time.sleep(1)
            action_passer("pics/loot/sec_summon.png")
        elif action_passer("pics/loot/normal_first.png"):
            time.sleep(1)
            action_passer("pics/loot/second_not_free.png")
        # else:
        #     print("Wrong Interface")
        #     break
        time.sleep(3)
        take_screenshot(screenshot_path, str(round) + "_round_beginning", window_name)
        count = 0
        for color in selected_colors:
            time.sleep(2)
            while color_checker(color,version_fold) or color_checker(color + "_hide",version_fold):
                count = count + 1
                time.sleep(2)
                if action_passer("pics/loot/next_summon.png"):
                    time.sleep(2)
                    color_checker(color,version_fold)
                time.sleep(2)
                action_passer("pics/loot/confirm.png")
                if color == "white":
                    print("因为是"+color+"开始检测是否错误： ",end= "")
                    if color_checker("green",version_fold):
                        print("warning 识别错啦！！！！")
                        take_screenshot(screenshot_path,
                                        "WARNING_" + str(round) + "_round_" + str(count + i) + "th_wishes",
                                        window_name)
                        action_passer("pics/loot/confirm.png")
                        time.sleep(15)
                elif color == "green":
                    print("因为是" + color + "开始检测是否错误： ", end="")
                    if color_checker("white",version_fold):
                        print("warning 识别错啦！！！！")
                        take_screenshot(screenshot_path,
                                        "WARNING_" + str(round) + "_round_" + str(count + i) + "th_wishes",
                                        window_name)
                        action_passer("pics/loot/confirm.png")
                        time.sleep(15)
                else:
                    time.sleep(20)
                take_screenshot(screenshot_path, str(round) + "_round_" + str(count + i) + "th_wishes", window_name)
                pyautogui.click()
                time.sleep(2)
                if action_passer_no_reaction("pics/loot/close_after.png"):
                    if count == 5:
                        take_screenshot(screenshot_path, str(round) + "_round_ending", window_name)
                    action_passer("pics/loot/close_after.png")

                time.sleep(2)

        if count == 0:
            count = count + 1
            for color in ["white", "green", "red", "blue"]:
                if color_checker(color,version_fold):
                    time.sleep(2)
                    action_passer("pics/loot/confirm.png")
                    time.sleep(20)
                    take_screenshot(screenshot_path, str(round) + "_round_" + str(count + i) + "wishes", window_name)
                    pyautogui.click()
                    time.sleep(2)
                    action_passer("pics/loot/close_after.png")
                    time.sleep(2)
                    take_screenshot(screenshot_path, str(round) + "_round_ending", window_name)
                    action_passer("pics/loot/back.png")
                    time.sleep(2)
                    action_passer("pics/loot/end.png")
                    time.sleep(2)
                    break
        else:
            time.sleep(2)
            if not os.path.isfile(screenshot_path + str(round) + "_round_ending" + ".png"):
                take_screenshot(screenshot_path, str(round) + "_round_ending", window_name)
            action_passer("pics/loot/back.png")
            time.sleep(2)
            action_passer("pics/loot/end.png")
            time.sleep(2)

        action_passer("pics/loot/close.png")
        if count == 5:
            i = i + count
            print("Lucky! 本次为第 " + str(round) + " 回合,本回合进行了 " + str(count) + "次抽取，总计：" + str(i))
            continue
        else:
            i = i + count
            print("本次为第 " + str(round) + " 回合,本回合进行了 " + str(count) + "次抽取，总计：" + str(i))


# # Get the window
# windows = gw.getWindowsWithTitle('雷电模拟器')
#
#
# if windows:  # If the list is not empty, meaning we found a window that matches
#     window = windows[0]  # Take the first window (there should only be one)
#     window.activate()
# "white","green","red","blue"
selected_color = ["red", "green"]
# 雷电模拟器
# MuMu模拟器12
loot_processing("", selected_color, 5, "MuMu模拟器12","colors_540p")

def count_images_containing_template(template_path, folder_path, threshold=0.8):
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)  # ensure the template is a color image
    if template is None:  # check if the image was correctly loaded
        # raise ValueError(f"Template image at {template_path} could not be loaded")
        return 0
    count = 0
    for filename in os.listdir(folder_path):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            image_path = os.path.join(folder_path, filename)
            image = cv2.imread(image_path, cv2.IMREAD_COLOR)  # ensure the image is a color image
            if image is None:  # check if the image was correctly loaded
                print(f"Image at {image_path} could not be loaded, skipping...")
                continue

            result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
            locations = np.where(result >= threshold)
            if len(locations[0]) > 0:  # if any matches were found
                count += 1

    return count


def check_champions(wanted, sample_path, pics_path):
    need_replace = []
    for key in wanted:
        counted = count_images_containing_template(sample_path + "/" + key + ".png", pics_path)
        print(counted)
        if counted >= wanted[key][1]:
            need_replace.append(wanted[key][0])
    return need_replace


# # Usage:
# dist_wanted = {"sample": ("red", 1), "sample2": ("blue", 1)}
# template_path = "C://Users/xzy19/Desktop/sample.png"
# folder_path = "C:\\Users\\xzy19\\PycharmProjects\\FEHAutoPlayer\\finished_wishes\\2023-06-19-06-00-06"
# print(count_images_containing_template(template_path, folder_path))
# check_champions(dist_wanted,"C://Users/xzy19/Desktop",folder_path)
