import os
import sys
import pygetwindow as gw
import time
import cv2
import pyautogui
import numpy as np
from datetime import datetime
from skimage.feature import match_template
from skimage.io import imread

x, y, width, height = None, None, None, None
x_offset, y_offset = 0, 0


class StdoutToFile:
    def __init__(self, filename):
        self.filename = filename
        self.original_stdout = sys.stdout

    def start(self):
        if not os.path.isdir(os.path.dirname(self.filename)):
            os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        sys.stdout = open(self.filename, 'a', encoding='utf-8')

    def stop(self):
        if sys.stdout != self.original_stdout:
            sys.stdout.close()
            sys.stdout = self.original_stdout


def is_valid_png_path(file_path):
    if os.path.exists(file_path) and os.path.isfile(file_path):
        if file_path.lower().endswith('.png'):
            return True
    return False


def take_screenshot(path, name, window_name):
    if not os.path.exists(path):
        os.makedirs(path)

    try:
        # window = gw.getWindowsWithTitle(window_name)[0]
        #
        # # Activate the window
        # window.activate()
        #
        # x, y, width, height = window.left, window.top, window.width, window.height

        # Capture a screenshot of the region
        screenshot = pyautogui.screenshot(region=(x, y, width, height))

        # Save the screenshot to a file
        screenshot.save(path + name + ".png")
    except gw.PyGetWindowException:
        print("Window not set up correctly")
    except Exception as e:
        print(e)
    # Get the coordinates of the window


def check_image_cv2(img_threshold, folder_path):
    matches = []

    # Take a screenshot of the screen
    # screenshot = pyautogui.screenshot()
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
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
            threshold = img_threshold
            locations = np.where(result >= threshold)
            template_matches = zip(*locations[::-1])
            matches.extend(template_matches)
            if matches:
                for match in matches:
                    icon_x, icon_y = match
                    return icon_x, icon_y


def check_image_skimage(img_threshold, folder_path):
    # Read the template and screenshot images
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    screenshot.save("screenshot.png")
    for filename in os.listdir(folder_path):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            template_path = os.path.join(folder_path, filename)

            # Read the template and screenshot images
            template = imread(template_path)
            screenshot = imread("screenshot.png")

            # Perform template matching using NCC
            result = match_template(screenshot, template)

            # Find the best match location
            match_location = np.unravel_index(np.argmax(result), result.shape)

            # Get the top-left coordinates of the matched region
            match_x, match_y = match_location[1], match_location[0]

            # Calculate the similarity score
            similarity_score = result[match_location]

            # Compare the similarity score with the threshold
            if similarity_score >= img_threshold:
                return match_x+10, match_y+10

    return None, None


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


def check_image_similar(action_threshold, template_path):
    template = cv2.imread(template_path, 0)

    # Take a screenshot of the screen
    screenshot = pyautogui.screenshot()
    screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    # Perform template matching
    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)

    # Set a threshold to determine matches
    threshold = action_threshold
    locations = np.where(result >= threshold)
    matches = zip(*locations[::-1])

    # Iterate over the matches
    for match in matches:
        icon_x, icon_y = match
        return icon_x, icon_y


def action_passer(threshold, path):
    unchanged = path
    path_replaced = unchanged.replace("pics/loot/", "")
    path_replaced = path_replaced.replace(".png", "")
    print(path_replaced, end=" ", flush=True)
    icon_x, icon_y = None, None
    for i in range(10):
        time.sleep(0.1)
        try:
            icon_x, icon_y = check_image_similar(threshold, path)
        except Exception as e:
            print("*", end="", flush=True)
        if icon_y is not None:
            pyautogui.moveTo(icon_x + x_offset, icon_y + y_offset)
            pyautogui.click()
            print("完成", flush=True)
            return True

    print(" 未发现", flush=True)
    return False


def action_passer_no_reaction(threshold, path):
    icon_x, icon_y = None, None
    for i in range(10):
        time.sleep(0.1)
        try:
            icon_x, icon_y = check_image_similar(threshold, path)
        except Exception as e:
            print("", end="", flush=True)
        if icon_y is not None:
            return True

    return False


def action_passer_with_color(path):
    print(path, end=" ", flush=True)
    icon_x, icon_y = None, None
    for i in range(15):
        time.sleep(0.1)
        try:
            icon_x, icon_y = check_image_similar_with_color(path)
        except Exception as e:
            print("*", end="", flush=True)
        if icon_y is not None:
            pyautogui.moveTo(icon_x + x_offset, icon_y + y_offset)
            pyautogui.click()
            print("完成", flush=True)
            return True

    print(" 未发现", flush=True)
    return False


def color_checker(mode, threshold, color, c_fold):
    print("查询颜色 " + color + " : ", end="", flush=True)
    icon_x, icon_y = None, None
    if mode == 1:
        print("OpenCV模式 ", end="", flush=True)
        for i in range(10):
            time.sleep(0.1)
            try:
                icon_x, icon_y = check_image_cv2(threshold, "pics/loot/" + c_fold + "/" + color + "_with_pos/")
            except Exception as e:
                print("*", end="", flush=True)
        if icon_y is not None:
            pyautogui.moveTo(x + icon_x + x_offset,y + icon_y + y_offset)
            pyautogui.click()
            print(" 完成", flush=True)
            return True

        print(" 未发现.", flush=True)
    elif mode == 2:
        print("Skimage模式 ", end="", flush=True)
        for i in range(2):
            time.sleep(0.1)
            try:
                icon_x, icon_y = check_image_skimage(threshold, "pics/loot/" + c_fold + "/" + color + "_with_pos/")
            except Exception as e:
                print("*", end="", flush=True)
        if icon_y is not None:
            pyautogui.moveTo(x + icon_x + x_offset, y + icon_y + y_offset)
            pyautogui.click()
            print(" 完成", flush=True)
            return True

        print(" 未发现.", flush=True)
    return False


def loot_processing(path1, input_colors, counting, window_name, version_fold, action_threshold, color_threshold,
                    target_num, target_path, mode):
    threshold = action_threshold
    selected_colors = input_colors
    if not os.path.exists(path1 + "finished_wishes/"):
        os.makedirs(path1 + "finished_wishes/")
    current_time = datetime.now()

    # Format it as a string
    time_string = current_time.strftime("%Y-%m-%d-%H-%M-%S")
    screenshot_path = path1 + "finished_wishes/" + time_string + "/"
    print("截图文件夹: " + screenshot_path, flush=True)
    round_count = 0
    i = 0
    take_screenshot(path1 + "finished_wishes/", time_string + "_" + str(round_count) + "_record_wish_pool", window_name)
    while i < counting:
        round_count = round_count + 1
        print("", flush=True)
        print("**********************************", flush=True)
        time.sleep(2)
        if action_passer(threshold, "pics/loot/free_summon.png"):
            time.sleep(1)
            action_passer(threshold, "pics/loot/sec_summon.png")
        elif action_passer(threshold, "pics/loot/normal_first.png"):
            time.sleep(1)
            action_passer(threshold, "pics/loot/second_not_free.png")
        else:
            print("Wrong Interface")
            exit()
        time.sleep(3)
        take_screenshot(screenshot_path, str(round_count) + "_round_beginning", window_name)
        count = 0
        for color in selected_colors:
            time.sleep(2)
            while color_checker(mode, color_threshold, color, version_fold) or color_checker(mode, color_threshold,
                                                                                             color + "_hide",
                                                                                             version_fold):
                count = count + 1
                time.sleep(2)
                if action_passer(threshold, "pics/loot/next_summon.png"):
                    time.sleep(2)
                    color_checker(mode, color_threshold, color, version_fold)
                time.sleep(2)
                action_passer(threshold, "pics/loot/confirm.png")
                time.sleep(1)
                if mode == 1:
                    if color == "white":
                        print("因为是" + color + "开始检测是否错误： ", end="", flush=True)
                        if color_checker(mode, color_threshold, "green", version_fold):
                            print("warning 识别错啦！！！！", flush=True)
                            take_screenshot(screenshot_path,
                                            "WARNING_" + str(round_count) + "_round_" + str(count + i) + "th_wishes",
                                            window_name)
                            action_passer(threshold, "pics/loot/confirm.png")
                    elif color == "green":
                        print("因为是" + color + "开始检测是否错误： ", end="", flush=True)
                        if color_checker(mode, color_threshold, "white", version_fold):
                            print("warning 识别错啦！！！！", flush=True)
                            take_screenshot(screenshot_path,
                                            "WARNING_" + str(round_count) + "_round_" + str(count + i) + "th_wishes",
                                            window_name)
                            action_passer(threshold, "pics/loot/confirm.png")

                time.sleep(25)
                take_screenshot(screenshot_path, str(round_count) + "_round_" + str(count + i) + "th_wishes",
                                window_name)
                pyautogui.click()
                time.sleep(2)
                if action_passer_no_reaction(threshold, "pics/loot/close_after.png"):
                    if count == 5:
                        take_screenshot(screenshot_path, str(round_count) + "_round_ending", window_name)
                    action_passer(threshold, "pics/loot/close_after.png")

                time.sleep(2)

        if count == 0:
            count = count + 1
            print("糟糕！运气好差，没有想要的颜色呢;(")
            for color in ["white", "green", "red", "blue"]:
                if color_checker(mode, color_threshold, color, version_fold):
                    time.sleep(2)
                    action_passer(threshold, "pics/loot/confirm.png")
                    time.sleep(23)
                    take_screenshot(screenshot_path, str(round_count) + "_round_" + str(count + i) + "wishes",
                                    window_name)
                    pyautogui.click()
                    time.sleep(2)
                    action_passer(threshold, "pics/loot/close_after.png")
                    time.sleep(2)
                    take_screenshot(screenshot_path, str(round_count) + "_round_ending", window_name)
                    action_passer(threshold, "pics/loot/back.png")
                    time.sleep(2)
                    action_passer(threshold, "pics/loot/end.png")
                    time.sleep(2)
                    break
        else:
            time.sleep(2)
            if not os.path.isfile(screenshot_path + str(round_count) + "_round_ending" + ".png"):
                take_screenshot(screenshot_path, str(round_count) + "_round_ending", window_name)
            action_passer(threshold, "pics/loot/back.png")
            time.sleep(2)
            action_passer(threshold, "pics/loot/end.png")
            time.sleep(2)

        action_passer(threshold, "pics/loot/close.png")

        i = i + count

        print("本次为第 " + str(round_count) + " 回合,本回合进行了 " + str(count) + "次抽取，总计：" + str(i),
              flush=True)
        if i >= counting:
            print("达到上限,结束")
            exit()
        if check_results(target_num, target_path, screenshot_path, action_threshold):
            exit()


def check_results(target_num, target_path, screenshot_path, threshold):
    if target_num > 0:
        print("开始检查出货结果： ", end="", flush=True)
        if is_valid_png_path(target_path):
            result_num = count_images_containing_template(target_path, screenshot_path, threshold)
            if result_num >= target_num:
                print("已抽取" + str(result_num) + "个目标角色", flush=True)
                print("达到目标")
                return True
            else:
                print("已抽取" + str(result_num) + "个目标角色", flush=True)
                print("未达到目标")
                return False
        else:
            print("目标文件不合规", flush=True)
            return False


def execute(path1, input_colors, counting, window_name, version_fold, log_path, button_thres, color_thres,
            target_num, target_path, mode_str, x_num, y_num):
    global x, y, width, height, x_offset, y_offset
    # print(path1, input_colors, counting, window_name, version_fold, log_path, button_thres, color_thres,
    # target_num, target_path, mode_str)
    stdout_to_file = StdoutToFile(log_path)
    stdout_to_file.start()

    print("||||||||||||||||||||||||||||||||||")
    print("当前设定:")
    # print("基础路径: ", end="")
    # print(path1)
    print("模板路径: ", end="")
    print(version_fold)
    print("选择颜色: ", end="")
    print(input_colors, end="")
    print(" ,抽取数量: ", end="")
    print(counting)
    print("窗口名: ", end="")
    print(window_name)
    print("日志文件名: ", end="")
    print(log_path)
    print("按键精度: ", end="")
    print(button_thres, end=" ， ")
    print("抽取精度: ", end="")
    print(color_thres)
    print("抽取目标: ", end="")
    print(target_path)
    print("抽取数量: ", end="")
    print(target_num)
    print("模式: ", end="")
    mode = int(mode_str)
    print(mode)
    print("X_offset: ", end="")
    print(x_num)
    print("Y_offset: ", end="")
    print(y_num)

    x_offset = x_num
    y_offset = y_num
    print("||||||||||||||||||||||||||||||||||", flush=True)
    try:

        window = gw.getWindowsWithTitle(window_name)[0]

        # Activate the window
        window.activate()

        # Get the coordinates of the window
        x, y, width, height = window.left, window.top, window.width, window.height
    except IndexError:
        print("未找到窗口，检查窗口名", flush=True)
        stdout_to_file.stop()
        exit()
    except Exception as e:
        print(e, end="", flush=True)
        stdout_to_file.stop()
        exit()
    loot_processing(path1, input_colors, counting, window_name, version_fold, button_thres, color_thres, target_num
                    , target_path, mode)
    stdout_to_file.stop()


def count_images_containing_template(template_path, folder_path, threshold):
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
                print("Image at " + image_path + " could not be loaded, skipping...", flush=True)
                continue

            result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
            locations = np.where(result >= threshold)
            if len(locations[0]) > 0:  # if any matches were found
                count += 1

    return count

# # Usage:
# dist_wanted = {"sample": ("red", 1), "sample2": ("blue", 1)}
# template_path = "C://Users/xzy19/Desktop/sample.png"
# folder_path = "C:\\Users\\xzy19\\PycharmProjects\\FEHAutoPlayer\\finished_wishes\\2023-06-19-06-00-06"
# print(count_images_containing_template(template_path, folder_path))
# check_champions(dist_wanted,"C://Users/xzy19/Desktop",folder_path)

# # Get the window
# windows = gw.getWindowsWithTitle('雷电模拟器')
#
#
# if windows:  # If the list is not empty, meaning we found a window that matches
#     window = windows[0]  # Take the first window (there should only be one)
#     window.activate()
# "white","green","red","blue"
# selected_color = ["white"]

# execute("", selected_color, 10, '模拟器', 'colors_leidian', 'logs/sample_log.txt', 0.7, 0.85,1, "C:/Users/xzy19/Desktop/123129.png", "2")

# 雷电模拟器
# MuMu模拟器12

# loot_processing("", selected_color, 5, "模拟器","colors_540p")
#
# window = gw.getWindowsWithTitle("模拟器")[0]
#
#         # Activate the window
# window.activate()
#
# x, y, width, height = window.left, window.top, window.width, window.height
# # pyautogui.moveTo(check_image(0.8, "pics/loot/colors_leidian/green_with_pos"))
# for i in range (30):
#     try:
#         print(check_image_skimage(0.85, "pics/loot/colors_leidian/green_hide_with_pos"))
#     except Exception as e:
#         print(e)
