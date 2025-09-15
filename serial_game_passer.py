import os
import sys
import pygetwindow as gw
import time
import cv2
import pyautogui
import numpy as np

# import contextlib

# import pytesseract

x, y, width, height = None, None, None, None
x_offset, y_offset = 0, 0

def skip_now_first(skip_mode,text, pass_threshold):

    time.sleep(2)
    with open(os.devnull, 'w') as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        st_flag = False
        # fight_action_passer("pics/aftergame_close.png")
        # time.sleep(1)
        if skip_mode == "1":
            if check_image_similar_with_control("pics/skip.png", pass_threshold) == False or check_image_similar_with_control("pics/skip_green.png", pass_threshold) == False:
                # time.sleep(300)
                print("chengle!!!!!!!!")
            while check_image_similar_with_control("pics/skip.png", pass_threshold) or check_image_similar_with_control(
                    "pics/skip_green.png", pass_threshold):
                pyautogui.moveTo((x + 20), (y + height / 2))
                pyautogui.click()
                time.sleep(5)
                st_flag = True
        elif skip_mode == "2":
            if fight_action_passer_with_control("pics/skip.png", pass_threshold) or fight_action_passer_with_control(
                    "pics/skip_green.png", pass_threshold):
                st_flag = True
        sys.stdout = old_stdout

        if st_flag:
            print(text + "skip SUCCESS", flush=True)
        else:
            print(text + "skip NOT FOUND", flush=True)

    time.sleep(2)

def skip_now(skip_mode,text, pass_threshold):

    time.sleep(2)
    with open(os.devnull, 'w') as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        st_flag = False
        # fight_action_passer("pics/aftergame_close.png")
        # time.sleep(1)
        if skip_mode == "1":
            while check_image_similar_with_control("pics/skip.png", pass_threshold) or check_image_similar_with_control("pics/skip_green.png", pass_threshold):
                pyautogui.moveTo((x + 20), (y + height / 2))
                pyautogui.click()
                time.sleep(5)
                st_flag = True
        elif skip_mode == "2":
            if fight_action_passer_with_control("pics/skip.png", pass_threshold) or fight_action_passer_with_control(
                    "pics/skip_green.png", pass_threshold):
                st_flag = True
        sys.stdout = old_stdout

        if st_flag:
            print(text + "skip SUCCESS", flush=True)
        else:
            print(text + "skip NOT FOUND", flush=True)

    time.sleep(2)


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


def check_image_main(folder_path, pass_threshold, mode):
    matches = []
    screenshot = pyautogui.screenshot()
    screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    if mode == 1:
        for filename in os.listdir(folder_path):
            if filename.endswith('.png') or filename.endswith('.jpg'):
                template_path = os.path.join(folder_path, filename)
                template = cv2.imread(template_path, 0)
                result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
                threshold = pass_threshold
                locations = np.where(result >= threshold)
                template_matches = zip(*locations[::-1])
                matches.extend(template_matches)
    elif mode == 2:

        threshold = pass_threshold

        matches = []
        screenshot = pyautogui.screenshot()
        screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
        proximity_threshold = 70

        exclusion_icon_path = "pics/main_ticked.png"
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
                    if not any(abs(ex[0] - match[0]) <= proximity_threshold and abs(
                            ex[1] - match[1]) <= proximity_threshold
                               for ex in exclusion_matches):
                        matches.append(match)

    for match in matches:
        icon_x, icon_y = match
        return icon_x, icon_y


def check_image_second(folder_path, pass_threshold, mode):
    matches = []
    screenshot = pyautogui.screenshot()
    screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    if mode == 1:
        for filename in os.listdir(folder_path):
            if filename.endswith('.png') or filename.endswith('.jpg'):
                template_path = os.path.join(folder_path, filename)
                template = cv2.imread(template_path, 0)
                result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
                threshold = pass_threshold
                locations = np.where(result >= threshold)
                template_matches = zip(*locations[::-1])
                matches.extend(template_matches)
    elif mode == 2:

        threshold = pass_threshold

        matches = []
        screenshot = pyautogui.screenshot()
        screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
        proximity_threshold = 70

        exclusion_icon_path = "pics/second_ticked.png"
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
                    if not any(abs(ex[0] - match[0]) <= proximity_threshold and abs(
                            ex[1] - match[1]) <= proximity_threshold
                               for ex in exclusion_matches):
                        matches.append(match)

    for match in matches:
        icon_x, icon_y = match
        return icon_x, icon_y


def main_stream_passer(difficulty, pass_threshold, mode_for_check):
    print("一级主界面", end="", flush=True)
    icon_x, icon_y = None, None
    for i in range(10):
        time.sleep(0.1)
        try:
            icon_x, icon_y = check_image_main("pics/first_level" + difficulty, pass_threshold, mode_for_check)
        except Exception as e:
            print("*", end="", flush=True)
        if icon_y is not None:
            pyautogui.moveTo(icon_x + x_offset, icon_y + y_offset)
            pyautogui.click()
            print("完成", flush=True)
            return True
    pyautogui.moveTo((x + 20), (y + height / 2))
    pyautogui.dragTo((x + 20), (y + height / 2 + 150), duration=1)
    time.sleep(1)

    print("未发现.", flush=True)
    return False


def main_stream_second_level_passer(difficulty, pass_threshold, mode_for_check):
    print("二级主界面", end="", flush=True)
    icon_x, icon_y = None, None
    for i in range(10):
        time.sleep(0.1)
        try:
            icon_x, icon_y = check_image_second("pics/second_level" + difficulty, pass_threshold, mode_for_check)
        except Exception as e:
            print("*", end="", flush=True)
        if icon_y is not None:
            pyautogui.moveTo(icon_x + x_offset, icon_y + y_offset)
            pyautogui.click()
            print("完成", flush=True)
            return True
    pyautogui.moveTo((x + 20), (y + height / 2))
    pyautogui.dragTo((x + 20), (y + height / 2 + 150), duration=1)
    time.sleep(1)
    print("未发现.", flush=True)
    return False


# def fight_action_passer(path):
#     print(path, end=" ", flush=True)
#     icon_x, icon_y = None, None
#     for i in range(5):
#         time.sleep(0.1)
#         try:
#             icon_x, icon_y = check_image_similar(path)
#         except Exception as e:
#             print("*", end="", flush=True)
#         if icon_y is not None:
#             pyautogui.moveTo(icon_x + 20, icon_y + 20)
#             pyautogui.click()
#             print("完成", flush=True)
#             return True
#
#     print(" 未发现.", flush=True)
#     return False

def end_image_checker(path, digit1):
    print(path, end=" ", flush=True)
    icon_x, icon_y = None, None
    for i in range(5):
        time.sleep(0.1)
        try:
            icon_x, icon_y = check_image_similar_with_control(path, digit1)
        except Exception as e:
            print("*", end="", flush=True)

        if icon_y is not None:
            time.sleep(1)
            icon_x_sec, icon_y_sec = None, None
            try:
                icon_x_sec, icon_y_sec = check_image_similar_with_control(path, digit1)
            except Exception as e:
                print("*", end="", flush=True)

            if icon_y_sec is not None:
                pyautogui.moveTo(icon_x + x_offset, icon_y + y_offset)
                pyautogui.click()
                print("完成", flush=True)
                return True

    print(" 未发现.", flush=True)
    return False

def fight_action_passer_with_control(path, digit1):
    print(path, end=" ", flush=True)
    icon_x, icon_y = None, None
    for i in range(5):
        time.sleep(0.1)
        try:
            icon_x, icon_y = check_image_similar_with_control(path, digit1)
        except Exception as e:
            print("*", end="", flush=True)
        if icon_y is not None:
            pyautogui.moveTo(icon_x + x_offset, icon_y + y_offset)
            pyautogui.click()
            print("完成", flush=True)
            return True

    print(" 未发现.", flush=True)
    return False


def start_fight(skip_mode,pass_threshold):
    # lower_threshold = 0.6
    # higher_threshold = 0.9
    if pass_threshold > 0.8:
        higher_threshold = 0.9
    else:
        higher_threshold = pass_threshold + 0.1
    if pass_threshold < 0.25:
        lower_threshold = 0.1
    else:
        lower_threshold = pass_threshold - 0.15
    if fight_action_passer_with_control("pics/haschamp.png", higher_threshold):
        time.sleep(2)
        fight_action_passer_with_control("pics/start_fight.png", pass_threshold)
        time.sleep(1)
        fight_action_passer_with_control("pics/refill.png", pass_threshold)
        time.sleep(2)
        fight_action_passer_with_control("pics/aftergame_close.png", pass_threshold)
        time.sleep(5)
        skip_now_first(skip_mode,"First", pass_threshold)
        pyautogui.click()
        skip_now(skip_mode,"Second", pass_threshold)
        fight_action_passer_with_control("pics/start_fight_ingame.png", pass_threshold)
        skip_now(skip_mode,"Third", pass_threshold)
        fight_action_passer_with_control("pics/auto_ingame.png", pass_threshold)
        time.sleep(2)
        fight_action_passer_with_control("pics/auto_confirm.png", pass_threshold)
        skip_now(skip_mode,"", pass_threshold)
        # time.sleep(20)

        print("start fetching end game image:", end=" ", flush=True)
        with open(os.devnull, 'w') as devnull:
            old_stdout = sys.stdout
            sys.stdout = devnull
            st_flag = False

            succes_count = 0
            for i in range(0, 1200):
                if fight_action_passer_with_control("pics/over.png", pass_threshold):
                    time.sleep(2)
                    fight_action_passer_with_control("pics/give_up.png", lower_threshold)
                    sys.stdout = old_stdout
                    print("Defeat!!!!!", flush=True)
                    exit()
                if fight_action_passer_with_control("pics/lose.png", lower_threshold):
                    time.sleep(2)
                    fight_action_passer_with_control("pics/give_up.png", lower_threshold)
                    time.sleep(2)
                    fight_action_passer_with_control("pics/start_again.png", lower_threshold)
                    time.sleep(2)
                    fight_action_passer_with_control("pics/start_again_2.png", lower_threshold)
                    time.sleep(2)
                    fight_action_passer_with_control("pics/start_fight_ingame.png", pass_threshold)
                    fight_action_passer_with_control("pics/start_again.png", lower_threshold)
                    time.sleep(2)
                    fight_action_passer_with_control("pics/start_again.png", lower_threshold)
                    time.sleep(2)
                    skip_now(skip_mode, "addition", pass_threshold)
                    fight_action_passer_with_control("pics/auto_ingame.png", pass_threshold)
                    time.sleep(2)
                    fight_action_passer_with_control("pics/auto_confirm.png", pass_threshold)
                    skip_now(skip_mode, "addition2", pass_threshold)
                    print("Lose and Continue!!!!!", flush=True)

                skip_now(skip_mode,"", pass_threshold)
                time.sleep(1)
                if end_image_checker("pics/stage_clear.png", pass_threshold):
                    st_flag = True
                    break
                elif end_image_checker("pics/stage_clear_part.png", higher_threshold):
                    st_flag = True
                    sys.stdout = old_stdout
                    print("备用验证成功", end=" ", flush=True)
                    break
            sys.stdout = old_stdout
            if st_flag:
                pyautogui.click()
                print("fetching SUCCESS", flush=True)
            else:
                print("fetching Failed", flush=True)

        time.sleep(2)
        pyautogui.moveTo((x + 20), (y + height / 2))
        pyautogui.click()
        skip_now(skip_mode,"First", pass_threshold)
        pyautogui.click()
        skip_now(skip_mode,"Second", pass_threshold)
        pyautogui.click()
        skip_now(skip_mode,"Thrid", pass_threshold)
        pyautogui.click()
        fight_action_passer_with_control("pics/aftergame_close.png", pass_threshold)
        time.sleep(1)
        fight_action_passer_with_control("pics/aftergame_close.png", pass_threshold)
        time.sleep(1)
        fight_action_passer_with_control("pics/aftergame_close.png", pass_threshold)
        time.sleep(1)
        fight_action_passer_with_control("pics/aftergame_close.png", pass_threshold)
        time.sleep(1)
        fight_action_passer_with_control("pics/aftergame_close.png", pass_threshold)
        time.sleep(1)
    else:
        time.sleep(2)
        fight_action_passer_with_control("pics/start_fight.png", pass_threshold)
        time.sleep(1)
        fight_action_passer_with_control("pics/refill.png", pass_threshold)
        time.sleep(2)
        fight_action_passer_with_control("pics/aftergame_close.png", pass_threshold)
        time.sleep(5)
        skip_now_first(skip_mode, "First", pass_threshold)
        pyautogui.click()
        skip_now(skip_mode,"Second ", pass_threshold)
        pyautogui.click()
        time.sleep(2)
        fight_action_passer_with_control("pics/start_fight_ingame.png", pass_threshold)
        skip_now(skip_mode,"Third ", pass_threshold)
        fight_action_passer_with_control("pics/auto_ingame.png", pass_threshold)
        time.sleep(2)
        fight_action_passer_with_control("pics/auto_confirm.png", pass_threshold)
        skip_now(skip_mode,"Final ", pass_threshold)
        # time.sleep(20)

        print("start fetching end game image:", end=" ", flush=True)
        with open(os.devnull, 'w') as devnull:
            old_stdout = sys.stdout
            sys.stdout = devnull
            st_flag = False
            for i in range(0, 1200):
                if fight_action_passer_with_control("pics/over.png", pass_threshold):
                    time.sleep(2)
                    fight_action_passer_with_control("pics/give_up.png", lower_threshold)
                    sys.stdout = old_stdout
                    print("Defeat!!!!!", flush=True)
                    exit()
                if fight_action_passer_with_control("pics/lose.png", lower_threshold):
                    time.sleep(2)
                    fight_action_passer_with_control("pics/give_up.png", lower_threshold)
                    time.sleep(2)
                    fight_action_passer_with_control("pics/start_again.png", lower_threshold)
                    time.sleep(2)
                    fight_action_passer_with_control("pics/start_again_2.png", lower_threshold)
                    time.sleep(2)
                    fight_action_passer_with_control("pics/start_fight_ingame.png", pass_threshold)
                    fight_action_passer_with_control("pics/start_again.png", lower_threshold)
                    time.sleep(2)
                    fight_action_passer_with_control("pics/start_again.png", lower_threshold)
                    time.sleep(2)
                    skip_now(skip_mode, "addition", pass_threshold)
                    fight_action_passer_with_control("pics/auto_ingame.png", pass_threshold)
                    time.sleep(2)
                    fight_action_passer_with_control("pics/auto_confirm.png", pass_threshold)
                    skip_now(skip_mode, "addition2", pass_threshold)
                    print("Lose and Continue!!!!!", flush=True)
                fight_action_passer_with_control("pics/skip.png", pass_threshold)
                time.sleep(1)
                if end_image_checker("pics/stage_clear.png", pass_threshold):
                    st_flag = True
                    break
                elif end_image_checker("pics/stage_clear_part.png", higher_threshold):
                    st_flag = True
                    sys.stdout = old_stdout
                    print("备用验证成功", end=" ", flush=True)
                    break
            sys.stdout = old_stdout

            if st_flag:
                pyautogui.click()
                print("fetching SUCCESS", flush=True)
            else:
                print("fetching Failed", flush=True)

        time.sleep(2)
        pyautogui.moveTo((x + 20), (y + height / 2))
        pyautogui.click()
        skip_now(skip_mode,"First ", pass_threshold)
        skip_now(skip_mode,"Second ", pass_threshold)
        skip_now(skip_mode,"Third ", pass_threshold)
        pyautogui.click()
        fight_action_passer_with_control("pics/aftergame_close.png", pass_threshold)
        time.sleep(1)
        skip_now(skip_mode,"羁绊 ", pass_threshold)
        fight_action_passer_with_control("pics/aftergame_close.png", pass_threshold)
        time.sleep(1)
        fight_action_passer_with_control("pics/aftergame_close.png", pass_threshold)
        time.sleep(1)
        fight_action_passer_with_control("pics/aftergame_close.png", pass_threshold)
        time.sleep(1)
        fight_action_passer_with_control("pics/aftergame_close.png", pass_threshold)
        time.sleep(1)


def test_current():
    x, y = pyautogui.position()
    print(x, y)


def second_level_iter(skip_mode,diff, pass_threshold, mode_for_check):
    while True:

        second_flag = main_stream_second_level_passer(diff, pass_threshold, mode_for_check)
        if not second_flag:
            print("检查是否返回一级", flush=True)
            first_flag = main_stream_passer(diff, pass_threshold, mode_for_check)
            if not first_flag:
                first_flag = main_stream_passer(diff, pass_threshold, mode_for_check)
            time.sleep(1)
            if first_flag:
                print("已回归一级", flush=True)
                return True
            else:
                print("未回归一级", end=" ", flush=True)
            second_flag = main_stream_second_level_passer(diff, pass_threshold, mode_for_check)
            if not second_flag:
                print("开始返回一级", flush=True)
                fight_action_passer_with_control("pics/backward.png", pass_threshold)
                return True
        time.sleep(2)
        start_fight(skip_mode,pass_threshold)


# def execute(diff, window_name, text_box):
def execute(diff, window_name, log_path, threshold, mode_of_check, x_num, y_num,skip):
    pass_threshold = float(threshold)
    global x, y, width, height, x_offset, y_offset
    stdout_to_file = StdoutToFile(log_path)
    stdout_to_file.start()
    skip_mode = skip
    print("||||||||||||||||||||||||||||||||||")
    print("当前设定:")
    print("模板路径: ", end="")
    print(diff)
    print("窗口名: ", end="")
    print(window_name)
    print("日志文件名: ", end="")
    print(log_path)
    print("精度: ", end="")
    print(threshold)
    print("Mode: ", end="")
    print(mode_of_check)
    print("X_offset: ", end="")
    print(x_num)
    print("Y_offset: ", end="")
    print(y_num)
    print("Skip Mode: ", end="")
    print(skip_mode, end="")
    x_offset = x_num
    y_offset = y_num

    mode_for_check = int(mode_of_check)
    # print(diff, window_name, log_path, threshold)
    try:
        # window = gw.getWindowsWithTitle('MuMu模拟器12')[0]

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
        exit()

    # sys.stdout = StdoutRedirector(text)

    try:
        switch_flag = True
        while switch_flag:

            print("|||||||Story Passer Started|||||||", flush=True)
            first_flag = main_stream_passer(diff, pass_threshold, mode_for_check)
            if not first_flag:
                first_flag = main_stream_passer(diff, pass_threshold, mode_for_check)
                if not first_flag:
                    print("未找到主界面，结束运行", flush=True)
                    print("|||||||Story Passer Ending||||||||", flush=True)
                    switch_flag = False
                    stdout_to_file.stop()
                    return True

                    # exit()

            time.sleep(1)
            if second_level_iter(skip_mode,diff, pass_threshold, mode_for_check):
                print("返回一级", flush=True)
    except Exception as e:
        print(e, end="", flush=True)
        stdout_to_file.stop()
        # exit()
    finally:
        stdout_to_file.stop()



class StdoutToFile:
    def __init__(self, filename):
        self.filename = filename
        self.original_stdout = sys.stdout

    def start(self):
        if not os.path.isdir(os.path.dirname(self.filename)):
            os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        sys.stdout = open(self.filename, 'a', encoding='utf-8')
        if sys.stdout != self.original_stdout:
            sys.stdout.close()
            sys.stdout = self.original_stdout

    def stop(self):
        if sys.stdout != self.original_stdout:
            sys.stdout.close()
            sys.stdout = self.original_stdout

# try:
#     while True:
#         auto_start("_hard")
# except KeyboardInterrupt:
#     print("Shut down by user")
# except Exception as e:
#     print(e, end="")

# print (check_image_similar())
# while True:
#     auto_start()
def menu_action_passer_with_control(path, digit1):
    print(path, end=" ", flush=True)
    icon_x, icon_y = None, None
    for i in range(5):
        time.sleep(0.1)
        try:
            icon_x, icon_y = check_image_similar_with_control(path, digit1)
        except Exception as e:
            print("*", end="", flush=True)
        if icon_y is not None:
            pyautogui.moveTo(icon_x , icon_y + y_offset)
            pyautogui.click()
            print("完成", flush=True)
            return True

    print(" 未发现.", flush=True)
    return False



def fuso_start_fight(skip_mode,pass_threshold,window_name):
    # lower_threshold = 0.6
    # higher_threshold = 0.9
    global x, y, width, height
    window = gw.getWindowsWithTitle(window_name)[0]

    # Activate the window
    window.activate()

    # Get the coordinates of the window
    x, y, width, height = window.left, window.top, window.width, window.height
    print (x, y, width, height)
    if pass_threshold > 0.8:
        higher_threshold = 0.9
    else:
        higher_threshold = pass_threshold + 0.1
    if pass_threshold < 0.25:
        lower_threshold = 0.1
    else:
        lower_threshold = pass_threshold - 0.15

        time.sleep(2)
        fight_action_passer_with_control("pics/start_fight.png", pass_threshold)
        time.sleep(1)
        fight_action_passer_with_control("pics/refill.png", pass_threshold)
        time.sleep(2)
        fight_action_passer_with_control("pics/aftergame_close.png", pass_threshold)

    for x in range(0, 5):
        time.sleep(5)
        print("###################", flush=True)
        # fight_action_passer_with_control("pics/refill.png", pass_threshold)
        pyautogui.click()
        fight_action_passer_with_control("pics/start_fight_ingame.png", pass_threshold)
        time.sleep(1)
        fight_action_passer_with_control("pics/minor_level_start.png", pass_threshold)
        time.sleep(2)
        skip_now(skip_mode,"First", pass_threshold)
        fight_action_passer_with_control("pics/start_fight_ingame.png", pass_threshold)
        skip_now(skip_mode,"Second", pass_threshold)
        fight_action_passer_with_control("pics/auto_ingame.png", pass_threshold)
        time.sleep(2)
        fight_action_passer_with_control("pics/auto_confirm.png", pass_threshold)
        skip_now(skip_mode,"", pass_threshold)
        # time.sleep(20)

        print("start fetching end game image:", end=" ", flush=True)
        with open(os.devnull, 'w') as devnull:
            old_stdout = sys.stdout
            sys.stdout = devnull
            st_flag = False

            succes_count = 0
            for i in range(0, 1200):
                if fight_action_passer_with_control("pics/over.png", pass_threshold):
                    time.sleep(2)
                    fight_action_passer_with_control("pics/give_up.png", lower_threshold)
                    sys.stdout = old_stdout
                    print("Defeat!!!!!", flush=True)
                    break
                if fight_action_passer_with_control("pics/lose.png", lower_threshold):
                    time.sleep(2)
                    fight_action_passer_with_control("pics/give_up.png", lower_threshold)
                    time.sleep(2)
                    fight_action_passer_with_control("pics/start_again.png", lower_threshold)
                    time.sleep(2)
                    fight_action_passer_with_control("pics/start_again_2.png", lower_threshold)
                    time.sleep(2)
                    fight_action_passer_with_control("pics/start_fight_ingame.png", pass_threshold)
                    fight_action_passer_with_control("pics/start_again.png", lower_threshold)
                    time.sleep(2)
                    fight_action_passer_with_control("pics/start_again.png", lower_threshold)
                    time.sleep(2)
                    skip_now(skip_mode, "addition", pass_threshold)
                    fight_action_passer_with_control("pics/auto_ingame.png", pass_threshold)
                    time.sleep(2)
                    fight_action_passer_with_control("pics/auto_confirm.png", pass_threshold)
                    skip_now(skip_mode, "addition2", pass_threshold)
                    print("Lose and Continue!!!!!", flush=True)

                skip_now(skip_mode,"", pass_threshold)
                time.sleep(1)
                if end_image_checker("pics/stage_clear.png", pass_threshold):
                    st_flag = True
                    break
                elif end_image_checker("pics/stage_clear_part.png", higher_threshold):
                    st_flag = True
                    sys.stdout = old_stdout
                    print("备用验证成功", end=" ", flush=True)
                    break
            sys.stdout = old_stdout
            if st_flag:
                pyautogui.click()
                print("fetching SUCCESS", flush=True)
            else:
                print("fetching Failed", flush=True)

    time.sleep(2)
    pyautogui.moveTo((x + 20), (y + height / 2))
    pyautogui.click()
    skip_now(skip_mode,"First", pass_threshold)
    pyautogui.click()
    skip_now(skip_mode,"Second", pass_threshold)
    pyautogui.click()
    skip_now(skip_mode,"Thrid", pass_threshold)
    pyautogui.click()
    fight_action_passer_with_control("pics/aftergame_close.png", pass_threshold)
    time.sleep(1)
    fight_action_passer_with_control("pics/aftergame_close.png", pass_threshold)
    time.sleep(1)
    fight_action_passer_with_control("pics/aftergame_close.png", pass_threshold)
    time.sleep(1)
    fight_action_passer_with_control("pics/aftergame_close.png", pass_threshold)
    time.sleep(1)
    fight_action_passer_with_control("pics/aftergame_close.png", pass_threshold)
    time.sleep(1)

# def fusuo():
#     global x, y, width, height
#     diff = "_serial"
#     window_name = "模拟器"
#     log_name = "logs/" + "test" + ".txt"
#     pass_threshold = 0.85
#     mode = 2
#     x_offset_num = 60
#     y_offset_num = 20
#     skip_mode = 1
#
#
#     try:
#         # window = gw.getWindowsWithTitle('MuMu模拟器12')[0]
#
#         window = gw.getWindowsWithTitle(window_name)[0]
#
#         # Activate the window
#         window.activate()
#
#         # Get the coordinates of the window
#         x, y, width, height = window.left, window.top, window.width, window.height
#         count = 0
#         while(True):
#             if count > 2:
#                 break
#
#             if main_stream_second_level_passer(diff,pass_threshold,2):
#                 fuso_start_fight(skip_mode, pass_threshold, window_name)
#
#             else:
#                 count = count + 1
#                 pyautogui.moveTo((x + 20), (y + height / 2))
#                 pyautogui.dragTo((x + 20), (y + height / 2 + 150), duration=1)
#                 time.sleep(1)
#     except IndexError:
#         print("未找到窗口，检查窗口名", flush=True)
#         exit()
#     except Exception as e:
#         print(e, end="", flush=True)
#         exit()

    # main_stream_second_level_passer(diff,pass_threshold,2)

# fusuo()

if __name__ == "__main__":
    diff = "_serial"
    # diff = ""
    window_name = "chaos"
    log_name = "logs/" + "test" + ".txt"
    pass_threshold = 0.9
    mode = 2
    x_offset_num = 60
    y_offset_num = 20
    skip_mode = 1

    while True:
        if menu_action_passer_with_control("pics/finish_chapter.png",0.85):
            if menu_action_passer_with_control("pics/next_cha_button.png",0.85):
                execute(diff, window_name, log_name, pass_threshold, mode,
                        x_offset_num, y_offset_num, skip_mode)
            else:
                exit()
        else:
            execute(diff, window_name, log_name, pass_threshold, mode,
                    x_offset_num, y_offset_num, skip_mode)
