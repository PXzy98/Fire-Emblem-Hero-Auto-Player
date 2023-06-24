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
# import pytesseract

x, y, width, height = None,None,None,None
def skip_now(text):
    time.sleep(2)
    with open(os.devnull, 'w') as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        st_flag = False
        # fight_action_passer("pics/aftergame_close.png")
        # time.sleep(1)
        if fight_action_passer("pics/skip.png") or fight_action_passer("pics/skip_green.png"):
            st_flag = True
        sys.stdout = old_stdout

        if st_flag:
            print(text + "skip SUCCESS")
        else:
            print(text + "skip NOT FOUND")

    time.sleep(2)


# def read_consume(path):
#     # Load the template image of the icon
#     target_image = cv2.imread(path)
#     x, y = None, None
#     try:
#         x, y = check_image_similar(path)
#     except Exception as e:
#         print("*", end="|")
#     if y is not None:
#         # top_left = (x - target_image.shape[1], y)
#         # top_right = (x, y)
#         # bottom_right = (x, y + target_image.shape[0])
#         # bottom_left = (x - target_image.shape[1], y + target_image.shape[0])
#
#         left = x - target_image.shape[1]
#         top = y
#         width = target_image.shape[1]
#         height = target_image.shape[0]
#
#         # Capture a screenshot of the region around the icon
#         screenshot = pyautogui.screenshot(region=(left, top, width, height))
#         screenshot.save("pics/screenshot.png")
#         image = cv2.imread("pics/screenshot.png")
#
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
#         # Invert the grayscale image to make the yellow text black
#         inverted = cv2.bitwise_not(gray)
#
#         # Apply adaptive thresholding
#         _, thresholded = cv2.threshold(inverted, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#
#         # Perform OCR on the thresholded image
#         text = pytesseract.image_to_string(thresholded)
#
#         # Extract numbers from the text
#         numbers = [int(word) for word in text.split() if word.isdigit()]
#
#         # Print the extracted numbers
#         print(numbers)
#     else:
#         print("Icon not found on the screen.")


def check_image_default(path):
    try:
        window = gw.getWindowsWithTitle('MuMu模拟器12')[0]

        # Activate the window
        window.activate()
        x, y, width, height = window.left, window.top, window.width, window.height

        # Move the mouse to a position within the window
        pyautogui.moveTo(x + 100, y + 100)
        pyautogui.click()
        icon_location = None
        for i in range(10):
            icon_location = pyautogui.locateOnScreen(path)
            time.sleep(0.1)

            if icon_location is not None:
                print(icon_location)
                break

        if icon_location is not None:
            # Get the center coordinates of the icon/picture
            icon_x, icon_y = pyautogui.center(icon_location)

            # Move the mouse to the icon/picture
            pyautogui.moveTo(icon_x, icon_y)
            pyautogui.click()
            return True
        else:
            exit()

            return False
    except Exception as e:
        print("An error occurred:", str(e))


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


def check_image_similar_with_control(template_path, digit1):
    template = cv2.imread(template_path, 0)

    # Take a screenshot of the screen
    screenshot = pyautogui.screenshot()
    screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    # Perform template matching
    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)

    # Set a threshold to determine matches
    threshold = digit1
    locations = np.where(result >= threshold)
    matches = zip(*locations[::-1])

    # Iterate over the matches
    for match in matches:
        icon_x, icon_y = match
        return icon_x, icon_y


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
    threshold = 0.9

    matches = []
    screenshot = pyautogui.screenshot()
    screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    proximity_threshold = 70

    exclusion_icon_path = "pics/cross.png"
    exclusion_icon_template = cv2.imread(exclusion_icon_path, 0)
    exclusion_result = cv2.matchTemplate(screenshot_gray, exclusion_icon_template, cv2.TM_CCOEFF_NORMED)
    exclusion_locations = np.where(exclusion_result >= threshold)
    exclusion_matches = set(zip(*exclusion_locations[::-1]))

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            template_path = os.path.join(folder_path, filename)
            template = cv2.imread(template_path, 0)
            result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
            locations = np.where(result >= threshold)
            template_matches = set(zip(*locations[::-1]))
            for match in template_matches:
                if not any(abs(ex[0] - match[0]) <= proximity_threshold and abs(ex[1] - match[1]) <= proximity_threshold
                           for ex in exclusion_matches):
                    matches.append(match)

    for match in matches:
        icon_x, icon_y = match
        return icon_x, icon_y


def main_stream_passer(difficulty):
    print("一级主界面", end="")
    icon_x, icon_y = None, None
    for i in range(10):
        time.sleep(0.1)
        try:
            icon_x, icon_y = check_image("pics/first_level" + difficulty)
        except Exception as e:
            print("*", end="")
        if icon_y is not None:
            pyautogui.moveTo(icon_x + 150, icon_y + 30)
            pyautogui.click()
            print("完成")
            return True
    pyautogui.moveTo((x + 20), (y + height / 2))
    pyautogui.dragTo((x + 20), (y + height / 2 + 150), duration=0.5)

    print("未发现.")
    return False


def main_stream_second_level_passer(difficulty):
    print("二级主界面", end="")
    icon_x, icon_y = None, None
    for i in range(10):
        time.sleep(0.1)
        try:
            icon_x, icon_y = check_image("pics/second_level" + difficulty)
        except Exception as e:
            print("*", end="")
        if icon_y is not None:
            pyautogui.moveTo(icon_x + 150, icon_y + 30)
            pyautogui.click()
            print("完成")
            return True
    pyautogui.moveTo((x + 20), (y + height / 2))
    pyautogui.dragTo((x + 20), (y + height / 2 + 150), duration=0.5)

    print("未发现.")
    return False


def fight_action_passer(path):
    print(path, end=" ")
    icon_x, icon_y = None, None
    for i in range(5):
        time.sleep(0.1)
        try:
            icon_x, icon_y = check_image_similar(path)
        except Exception as e:
            print("*", end="")
        if icon_y is not None:
            pyautogui.moveTo(icon_x + 20, icon_y+20)
            pyautogui.click()
            print("完成")
            return True

    print(" 未发现.")
    return False


def fight_action_passer_with_control(path, digit1):
    print(path, end=" ")
    icon_x, icon_y = None, None
    for i in range(5):
        time.sleep(0.1)
        try:
            icon_x, icon_y = check_image_similar_with_control(path, digit1)
        except Exception as e:
            print("*", end="")
        if icon_y is not None:
            pyautogui.moveTo(icon_x + 20, icon_y)
            pyautogui.click()
            print("完成")
            return True

    print(" 未发现.")
    return False


def start_fight():
    if fight_action_passer_with_control("pics/haschamp.png", 0.9):
        time.sleep(2)
        fight_action_passer("pics/start_fight.png")
        time.sleep(1)
        fight_action_passer("pics/refill.png")
        time.sleep(2)
        fight_action_passer("pics/aftergame_close.png")
        time.sleep(2)
        pyautogui.click()
        skip_now("")
        pyautogui.click()
        skip_now("")
        fight_action_passer("pics/start_fight_ingame.png")
        skip_now("")
        fight_action_passer("pics/auto_ingame.png")
        time.sleep(2)
        fight_action_passer("pics/auto_confirm.png")
        skip_now("")
        # time.sleep(20)

        print("start fetching end game image:", end=" ")
        with open(os.devnull, 'w') as devnull:
            old_stdout = sys.stdout
            sys.stdout = devnull
            st_flag = False
            for i in range(0, 120):
                if fight_action_passer("pics/over.png"):
                    time.sleep(2)
                    fight_action_passer_with_control("pics/give_up.png", 0.6)
                    sys.stdout = old_stdout
                    print("Defeat!!!!!")
                    exit()
                fight_action_passer("pics/skip.png")
                time.sleep(1)
                if fight_action_passer_with_control("pics/stage_clear.png", 0.8):
                    st_flag = True
                    break
                elif fight_action_passer_with_control("pics/stage_clear_part.png", 0.9):
                    st_flag = True
                    sys.stdout = old_stdout
                    print("备用验证成功", end=" ")
                    break
            sys.stdout = old_stdout
            if st_flag:
                pyautogui.click()
                print("fetching SUCCESS")
            else:
                print("fetching Failed")

        time.sleep(2)
        pyautogui.click()
        skip_now("First")
        pyautogui.click()
        skip_now("Second")
        skip_now("Thrid")
        pyautogui.click()
        fight_action_passer("pics/aftergame_close.png")
        time.sleep(1)
        fight_action_passer("pics/aftergame_close.png")
        time.sleep(1)
        fight_action_passer("pics/aftergame_close.png")
        time.sleep(1)
        fight_action_passer("pics/aftergame_close.png")
        time.sleep(1)
        fight_action_passer("pics/aftergame_close.png")
        time.sleep(1)
    else:
        time.sleep(2)
        fight_action_passer("pics/start_fight.png")
        time.sleep(1)
        fight_action_passer("pics/refill.png")
        time.sleep(2)
        fight_action_passer("pics/aftergame_close.png")
        time.sleep(2)
        pyautogui.click()
        skip_now("")
        pyautogui.click()
        skip_now("")
        pyautogui.click()
        time.sleep(2)
        fight_action_passer("pics/start_fight_ingame.png")
        skip_now("")
        fight_action_passer("pics/auto_ingame.png")
        time.sleep(2)
        fight_action_passer("pics/auto_confirm.png")
        skip_now("")
        # time.sleep(20)

        print("start fetching end game image:", end=" ")
        with open(os.devnull, 'w') as devnull:
            old_stdout = sys.stdout
            sys.stdout = devnull
            st_flag = False
            for i in range(0, 120):
                if fight_action_passer("pics/over.png"):
                    time.sleep(2)
                    fight_action_passer_with_control("pics/give_up.png", 0.6)
                    sys.stdout = old_stdout
                    print("Defeat!!!!!")
                    exit()
                fight_action_passer("pics/skip.png")
                time.sleep(1)
                if fight_action_passer_with_control("pics/stage_clear.png", 0.8):
                    st_flag = True
                    break
                elif fight_action_passer_with_control("pics/stage_clear_part.png", 0.9):
                    st_flag = True
                    sys.stdout = old_stdout
                    print("备用验证成功", end=" ")
                    break
            sys.stdout = old_stdout

            if st_flag:
                pyautogui.click()
                print("fetching SUCCESS")
            else:
                print("fetching Failed")

        time.sleep(2)
        pyautogui.click()
        skip_now("First ")
        skip_now("Second ")
        skip_now("Third ")
        pyautogui.click()
        fight_action_passer("pics/aftergame_close.png")
        time.sleep(1)
        fight_action_passer("pics/aftergame_close.png")
        time.sleep(1)
        fight_action_passer("pics/aftergame_close.png")
        time.sleep(1)
        fight_action_passer("pics/aftergame_close.png")
        time.sleep(1)
        fight_action_passer("pics/aftergame_close.png")
        time.sleep(1)


def test_current():
    x, y = pyautogui.position()
    print(x, y)


def second_level_iter(diff):
    while True:

        second_flag = main_stream_second_level_passer(diff)
        if not second_flag:
            print("检查是否返回一级")
            first_flag = main_stream_passer(diff)
            if not first_flag:
                first_flag = main_stream_passer(diff)
            time.sleep(1)
            if first_flag:
                print("已回归二级")
            else:
                print("未回归一级", end=" ")
            second_flag = main_stream_second_level_passer(diff)
            if not second_flag:
                print("二级完成")
                fight_action_passer("pics/backward.png")
                return True
        time.sleep(2)
        start_fight()


def auto_start(dif):
    print("|||||||Story Passer Starter|||||||")
    first_flag = main_stream_passer(dif)
    if not first_flag:
        first_flag = main_stream_passer(dif)
        if not first_flag:
            print("未找到主界面，结束运行")
            print("|||||||Story Passer Ending|||||||")
            exit()
    time.sleep(1)
    if second_level_iter(dif):
        print("second done")


def excute(diff,window_name):
    global x, y, width, height
    # window = gw.getWindowsWithTitle('MuMu模拟器12')[0]
    window = gw.getWindowsWithTitle(window_name)[0]

    # Activate the window
    window.activate()

    # Get the coordinates of the window
    x, y, width, height = window.left, window.top, window.width, window.height

    try:
        while True:
            auto_start(diff)
    except Exception as e:
        print(e, end="")

# try:
#     while True:
#         auto_start("_hard")
# except KeyboardInterrupt:
#     print("Shut down by user")
# except Exception as e:
#     print(e, end="")

# read_consume("pics/99.png")

# print (check_image_similar())
# while True:
#     auto_start()
