import multiprocessing
import os
import sys
import tkinter as tk
from datetime import datetime
# from threading import Thread, Event
from tkinter import ttk, filedialog
import time
import configparser
import story_passer
import loot_helper
import math
import pygetwindow as gw


class PasserProcess:

    # def __init__(self, difficulty, window_name):
    def __init__(self, difficulty, window_name, log_file, general_threshold, mode, x_offset, y_offset):
        self.mode = mode
        self.diff = difficulty
        self.window_name = window_name
        self.log_name = log_file
        self.pass_threshold = general_threshold
        self.x_offset_num = int(x_offset)
        self.y_offset_num = int(y_offset)
        self.process = None
        self.stop_event = multiprocessing.Event()
        self.queue = multiprocessing.Queue()

    def start(self):
        if self.process is not None and self.process.is_alive():
            return

        self.stop_event.clear()
        self.process = multiprocessing.Process(target=self.run_loop)
        self.process.start()

    def stop(self):
        if self.process is None or not self.process.is_alive():
            return

        self.stop_event.set()
        # self.process.join()
        self.process.terminate()
        self.process.join()

    def update(self, difficulty, window_name, log_file, general_threshold, mode, x_offset, y_offset):
        self.diff = difficulty
        self.window_name = window_name
        self.log_name = log_file
        self.pass_threshold = general_threshold
        self.mode = mode
        self.x_offset_num = int(x_offset)
        self.y_offset_num = int(y_offset)

    def run_loop(self):
        while not self.stop_event.is_set():
            # Processing logic

            result = story_passer.execute(self.diff, self.window_name, self.log_name, self.pass_threshold, self.mode,
                                          self.x_offset_num, self.y_offset_num)
            # result = story_passer.execute()

            # Update GUI by putting data in the queue
            self.queue.put(result)


class LootProcess:

    # def __init__(self, difficulty, window_name):
    def __init__(self, window_name, color_threshold, button_threshold, template_path, wish, log_file, selected_colors,
                 target_num, target_path, mode_num, x_offset, y_offset):
        # print((window_name, color_threshold, button_threshold, template_path, wish, log_file, selected_colors))
        self.selected_colors = selected_colors
        self.color_threshold = color_threshold
        self.button_threshold = button_threshold
        self.template_path = template_path
        self.wish = wish
        self.window_name = window_name
        self.log_name = log_file
        self.target_img_num = target_num
        self.template_img_path = target_path
        self.mode = mode_num
        self.process = None
        self.stop_event = multiprocessing.Event()
        self.queue = multiprocessing.Queue()
        self.x_offset_num = int(x_offset)
        self.y_offset_num = int(y_offset)

    def start(self):
        if self.process is not None and self.process.is_alive():
            return

        self.stop_event.clear()
        self.process = multiprocessing.Process(target=self.run_loop)
        self.process.start()

    def stop(self):
        if self.process is None or not self.process.is_alive():
            return

        self.stop_event.set()
        # self.process.join()
        self.process.terminate()
        self.process.join()

    def update(self, window_name, color_threshold, button_threshold, template_path, wish, log_file, selected_colors,
               target_num, target_path, mode_num, x_offset, y_offset):
        self.selected_colors = selected_colors
        self.color_threshold = color_threshold
        self.button_threshold = button_threshold
        self.template_path = template_path
        self.wish = wish
        self.window_name = window_name
        self.log_name = log_file
        self.target_img_num = target_num
        self.template_img_path = target_path
        self.mode = mode_num
        self.x_offset_num = int(x_offset)
        self.y_offset_num = int(y_offset)

    def run_loop(self):
        while not self.stop_event.is_set():
            # Processing logic loot_processing("", selected_color, 5, "模拟器", "colors_540p") path1, input_colors,
            # counting, window_name, version_fold result = loot_helper.loot_processing("", self.selected_colors,
            # self.wish,self.window_name, self.template_path)
            result = loot_helper.execute("", self.selected_colors, self.wish, self.window_name, self.template_path
                                         , self.log_name, self.button_threshold, self.color_threshold,
                                         self.target_img_num, self.template_img_path, self.mode, self.x_offset_num
                                         , self.y_offset_num)
            # result = loot_helper.loot_processing("", self.selected_colors, self.wish,self.window_name,
            # self.template_path,self.log_name) result = story_passer.execute()

            # Update GUI by putting data in the queue
            self.queue.put(result)


class RunningFrame(tk.Frame):

    # def __init__(self, i_frame, master=None, **kwargs):
    #
    #
    def __init__(self, i_frame, log_name, master=None, **kwargs):
        #
        #
        #
        super().__init__(master, **kwargs)
        # self.difficulty = difficulty
        # self.window_name = window_name
        # self.text_obj = text_obj
        self.log_name = log_name
        self.config_file = "config/config_passer.ini"
        self.config = configparser.ConfigParser()

        self.create_config_file_if_not_exists()

        self.config.read(self.config_file)

        input_area = ttk.LabelFrame(i_frame, text="Input_Area")
        input_area.grid(row=1, column=0, padx=10, pady=10)
        window_name_label = tk.Label(input_area, text="window_name:")
        window_name_label.grid(row=0, column=0, padx=10, pady=10)
        self.window_name_entry = tk.Entry(input_area, width=50)
        self.window_name_entry.grid(row=0, column=1, padx=10, pady=10)

        # Create a label for the template path and a text entry field
        template_path_label = tk.Label(input_area, text="template_path:")
        template_path_label.grid(row=1, column=0, padx=10, pady=10)
        self.template_path_entry = tk.Entry(input_area, width=50)
        self.template_path_entry.grid(row=1, column=1, padx=10, pady=10, columnspan=3)

        label = tk.Label(input_area, text="Thresholds :")
        label.grid(row=3, column=0, padx=10, pady=10)

        # Create a scale (slider) for values between 0 and 1
        self.slider = tk.Scale(input_area, from_=0, to=1, resolution=0.01, orient="horizontal", length=250)
        self.slider.grid(row=3, column=1, padx=10, pady=10)
        self.mode_var = tk.StringVar()
        # p1 = PasserProcess(diff, window_name)

        # Create a variable to store the selected mode
        radio_frame = tk.Frame(input_area)
        radio_frame.grid(row=4, column=0, columnspan=2)
        mode_label = tk.Label(radio_frame, text="mode:")
        mode_label.grid(row=0, column=0, padx=10, pady=10)
        # Create the radio button options
        radio_option1 = tk.Radiobutton(radio_frame, text="不排除钩子算法", variable=self.mode_var, value="1")
        radio_option1.grid(row=0, column=1, padx=5, pady=5)

        radio_option2 = tk.Radiobutton(radio_frame, text="排除钩子算法", variable=self.mode_var, value="2")
        radio_option2.grid(row=0, column=2, padx=5, pady=5)
        offset_frame = tk.Frame(input_area)
        offset_frame.grid(row=5, column=0, columnspan=4)
        self.x_label = tk.Label(offset_frame, text="X_offset", anchor='e', justify='left')
        self.x_label.grid(row=0, column=0, padx=2)

        self.x_slider = tk.Scale(offset_frame, from_=-300, to=300, resolution=10, orient="horizontal", length=150)
        self.x_slider.set(0)
        self.x_slider.grid(row=0, column=1, padx=2)

        self.y_label = tk.Label(offset_frame, text="Y_offset", anchor='e', justify='left')
        self.y_label.grid(row=0, column=2, padx=2)

        self.y_slider = tk.Scale(offset_frame, from_=-200, to=200, resolution=10, orient="horizontal", length=150)
        self.y_slider.set(0)
        self.y_slider.grid(row=0, column=3, padx=2)

        button_frame = tk.Frame(input_area)
        button_frame.grid(row=6, column=0, columnspan=2)

        self.p1 = PasserProcess(self.template_path_entry.get(), self.window_name_entry.get(), self.log_name,
                                self.slider.get(), self.mode_var.get(), self.x_slider.get(), self.y_slider.get())

        start_button = tk.Button(button_frame, text="Start", command=self.p_start)
        start_button.grid(row=0, column=3, padx=20, pady=5)
        stop_button = tk.Button(button_frame, text="Stop", command=self.p1.stop)
        stop_button.grid(row=0, column=4, padx=20, pady=5)
        save_button = tk.Button(button_frame, text="Save", command=self.save_config)
        save_button.grid(row=0, column=5, padx=20, pady=5)

        self.load_config_into_text_box()

    def p_start(self):
        self.p1.update(self.template_path_entry.get(), self.window_name_entry.get(), self.log_name, self.slider.get(),
                       self.mode_var.get(), self.x_slider.get(), self.y_slider.get())
        self.p1.start()

    def create_config_file_if_not_exists(self):
        directory = os.path.dirname(self.config_file)
        if not os.path.isdir(directory):
            os.makedirs(directory, exist_ok=True)

        if not os.path.isfile(self.config_file):
            self.config['Settings'] = {'window_name': 'MuMu模拟器12', 'pass_threshold': '0.7', 'template_path': '_hard',
                                       'mode': "1", 'x_offset': '0', "y_offset": "0"}
            with open(self.config_file, 'w') as file:
                self.config.write(file)

    def load_config_into_text_box(self):
        window_name = self.config.get('Settings', 'window_name', fallback='')
        pass_threshold = self.config.get('Settings', 'pass_threshold', fallback='')
        template_path = self.config.get('Settings', 'template_path', fallback='')
        mode = self.config.get('Settings', 'mode', fallback='')
        x_offset = self.config.get('Settings', 'x_offset', fallback='')
        y_offset = self.config.get('Settings', 'y_offset', fallback='')
        x, y, width, height = 0, 0, 0, 0
        try:
            window = gw.getWindowsWithTitle(window_name)[0]

            # Activate the window
            window.activate()

            x, y, width, height = window.left, window.top, window.width, window.height

        except Exception as e:
            x, y, width, height = 0, 0, 900, 600

        x_range = round(width / 3, -2)
        y_range = round(height / 3, -2)

        self.x_slider.config(from_=-x_range, to=x_range)
        self.y_slider.config(from_=-y_range, to=y_range)
        self.mode_var.set(mode)
        self.window_name_entry.insert(tk.END, window_name)
        self.template_path_entry.insert(tk.END, template_path)
        self.slider.set(float(pass_threshold))
        self.x_slider.set(int(x_offset))
        self.y_slider.set(int(y_offset))
        # print(pass_threshold)
        # return default_value

    def save_config(self):
        window_name = self.window_name_entry.get()
        pass_threshold = self.slider.get()
        template_path = self.template_path_entry.get()
        mode = self.mode_var.get()
        x_offset = self.x_slider.get()
        y_offset = self.y_slider.get()
        self.config['Settings'] = {'window_name': window_name, 'pass_threshold': pass_threshold,
                                   'template_path': template_path, 'mode': mode,
                                   'x_offset': x_offset, "y_offset": y_offset}
        with open(self.config_file, 'w') as file:
            self.config.write(file)


class RunningFrame2(tk.Frame):

    # def __init__(self, i_frame, master=None, **kwargs):
    #
    #
    def __init__(self, i_frame, log_name, master=None, **kwargs):
        #
        #
        #
        super().__init__(master, **kwargs)
        # self.difficulty = difficulty
        # self.window_name = window_name
        # self.text_obj = text_obj
        self.log_name = log_name
        self.config_file = "config/config_loot.ini"
        self.config = configparser.ConfigParser()

        self.create_config_file_if_not_exists()

        self.config.read(self.config_file)

        input_area = ttk.LabelFrame(i_frame, text="Input_Area")
        input_area.grid(row=1, column=0, padx=10, pady=10)
        window_name_label = tk.Label(input_area, text="window_name:")
        window_name_label.grid(row=0, column=0, padx=10, pady=10)
        self.window_name_entry = tk.Entry(input_area, width=50)
        self.window_name_entry.grid(row=0, column=1, padx=10, pady=10)

        # Create a label for the template path and a text entry field
        template_path_label = tk.Label(input_area, text="template_path:")
        template_path_label.grid(row=1, column=0, padx=10, pady=10)
        self.template_path_entry = tk.Entry(input_area, width=50)
        self.template_path_entry.grid(row=1, column=1, padx=10, pady=10, columnspan=3)

        slider_frame = tk.Frame(input_area)
        slider_frame.grid(row=2, column=0, columnspan=2)

        label = tk.Label(slider_frame, text="Wishes Thresholds :")
        label.grid(row=0, column=0, padx=10, pady=10)

        # Create a scale (slider) for values between 0 and 1
        self.slider1 = tk.Scale(slider_frame, from_=0, to=1, resolution=0.01, orient="horizontal", length=150)
        self.slider1.grid(row=0, column=1, padx=10, pady=10)
        self.mode_var = tk.StringVar()

        label = tk.Label(slider_frame, text="Button Thresholds :")
        label.grid(row=1, column=0, padx=10, pady=10)
        self.slider2 = tk.Scale(slider_frame, from_=0, to=1, resolution=0.01, orient="horizontal", length=150)
        self.slider2.grid(row=1, column=1, padx=10, pady=10)

        label = tk.Label(slider_frame, text="Wish Number :")
        label.grid(row=2, column=0, padx=10, pady=10)
        self.slider3 = tk.Scale(slider_frame, from_=1, to=40, resolution=1, orient="horizontal", length=250)
        self.slider3.grid(row=2, column=1, padx=10, pady=10)

        selection_frame = tk.Frame(input_area)
        selection_frame.grid(row=3, column=0, columnspan=2)

        # p1 = PasserProcess(diff, window_name)
        self.colors = ['white', 'green', 'blue', 'red']
        self.selected_colors = []

        self.check_buttons = []
        for i, color in enumerate(self.colors):
            var = tk.IntVar()
            checkbutton = tk.Checkbutton(selection_frame, text=color, variable=var, command=self.update_selection)
            checkbutton.grid(row=0, column=i, padx=5, pady=5)
            self.check_buttons.append((color, var))

        target_path_label = tk.Label(selection_frame, text="target_path:")
        target_path_label.grid(row=1, column=0, padx=10, pady=10)

        select_button = tk.Button(selection_frame, text="Select", command=self.open_file_dialog)
        select_button.grid(row=1, column=1, padx=5, pady=5)
        quantity_label = tk.Label(selection_frame, text="quantity:")
        quantity_label.grid(row=1, column=2, padx=10, pady=10)
        self.slider4 = tk.Scale(selection_frame, from_=0, to=10, resolution=1, orient="horizontal", length=150)
        self.slider4.set(0)
        self.slider4.grid(row=1, column=3, padx=10, pady=10)

        self.result_label = tk.Label(selection_frame, text="", width=60, anchor='e', justify='left')
        self.result_label.grid(row=2, column=0, pady=5, columnspan=4)
        offset_frame = tk.Frame(selection_frame)
        offset_frame.grid(row=3, column=0, columnspan=4)
        self.x_label = tk.Label(offset_frame, text="X_offset", anchor='e', justify='left')
        self.x_label.grid(row=0, column=0, padx=2)
        self.x_slider = tk.Scale(offset_frame, from_=-200, to=200, resolution=10, orient="horizontal", length=150)
        self.x_slider.set(0)
        self.x_slider.grid(row=0, column=1, padx=2)
        self.y_label = tk.Label(offset_frame, text="Y_offset", anchor='e', justify='left')
        self.y_label.grid(row=0, column=2, padx=2)
        self.y_slider = tk.Scale(offset_frame, from_=-200, to=200, resolution=10, orient="horizontal", length=150)
        self.y_slider.set(0)
        self.y_slider.grid(row=0, column=3, padx=2)
        mode_label = tk.Label(selection_frame, text="mode:")
        mode_label.grid(row=4, column=0, padx=10, pady=10)
        # Create the radio button options
        self.mode_var = tk.StringVar()
        radio_option1 = tk.Radiobutton(selection_frame, text="OpenCV", variable=self.mode_var, value="1")
        radio_option1.grid(row=4, column=1, padx=5, pady=5)

        radio_option2 = tk.Radiobutton(selection_frame, text="Skimage", variable=self.mode_var, value="2")
        radio_option2.grid(row=4, column=2, padx=5, pady=5)
        button_frame = tk.Frame(input_area)
        button_frame.grid(row=5, column=0, columnspan=2)
        # Create a variable to store the selected mode
        # window_name, color_threshold, button_threshold, template_path, wish, log_file, selected_colors
        self.p1 = LootProcess(self.window_name_entry.get(), self.slider1.get(), self.slider2.get(),
                              self.template_path_entry.get(), self.slider3.get(), self.log_name, self.selected_colors,
                              self.slider4.get(), self.result_label.cget('text'), self.mode_var.get(),
                              self.x_slider.get(), self.y_slider.get())

        start_button = tk.Button(button_frame, text="Start", command=self.p_start)
        start_button.grid(row=0, column=3, padx=20, pady=5)
        stop_button = tk.Button(button_frame, text="Stop", command=self.p1.stop)
        stop_button.grid(row=0, column=4, padx=20, pady=5)
        save_button = tk.Button(button_frame, text="Save", command=self.save_config)
        save_button.grid(row=0, column=5, padx=20, pady=5)

        self.load_config_into_text_box()

    def open_file_dialog(self):
        # Open file dialog and retrieve the selected file name
        file_path = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png")])

        if file_path:
            # Process the selected file
            self.result_label.config(text=file_path)

    def p_start(self):
        self.p1.update(self.window_name_entry.get(), self.slider1.get(), self.slider2.get(),
                       self.template_path_entry.get(), self.slider3.get(), self.log_name, self.selected_colors
                       , self.slider4.get(), self.result_label.cget('text'), self.mode_var.get(), self.x_slider.get(),
                       self.y_slider.get())
        self.p1.start()

    def create_config_file_if_not_exists(self):
        directory = os.path.dirname(self.config_file)
        if not os.path.isdir(directory):
            os.makedirs(directory, exist_ok=True)

        if not os.path.isfile(self.config_file):
            self.config['Settings'] = {'window_name': '模拟器', 'color_threshold': '0.9', 'button_threshold': '0.7',
                                       'template_path': 'colors_540p', 'wish': 5, 'mode': '1', 'x_offset': '0',
                                       "y_offset": "0"}
            with open(self.config_file, 'w') as file:
                self.config.write(file)

    def load_config_into_text_box(self):
        window_name = self.config.get('Settings', 'window_name', fallback='')
        color_threshold = self.config.get('Settings', 'color_threshold', fallback='')
        button_threshold = self.config.get('Settings', 'button_threshold', fallback='')
        template_path = self.config.get('Settings', 'template_path', fallback='')
        wish = self.config.get('Settings', 'wish', fallback='')
        mode = self.config.get('Settings', 'mode', fallback='')
        x_offset = self.config.get('Settings', 'x_offset', fallback='')
        y_offset = self.config.get('Settings', 'y_offset', fallback='')

        x, y, width, height = 0, 0, 0, 0
        try:
            window = gw.getWindowsWithTitle(window_name)[0]

            # Activate the window
            window.activate()

            x, y, width, height = window.left, window.top, window.width, window.height

        except Exception as e:
            x, y, width, height = 0, 0, 900, 600

        x_range = round(width / 3, -2)
        y_range = round(height / 3, -2)

        self.x_slider.config(from_=-x_range, to=x_range)
        self.y_slider.config(from_=-y_range, to=y_range)

        self.mode_var.set(mode)
        self.slider3.set(wish)
        self.slider2.set(button_threshold)
        self.slider1.set(color_threshold)
        self.x_slider.set(int(x_offset))
        self.y_slider.set(int(y_offset))

        self.window_name_entry.insert(tk.END, window_name)
        self.template_path_entry.insert(tk.END, template_path)

        # print(pass_threshold)
        # return default_value

    def save_config(self):
        color_threshold = self.slider1.get()
        button_threshold = self.slider2.get()
        wish = self.slider3.get()
        window_name = self.window_name_entry.get()
        template_path = self.template_path_entry.get()
        mode = self.mode_var.get()
        x_offset = self.x_slider.get()
        y_offset = self.y_slider.get()
        self.config['Settings'] = {'window_name': window_name, 'color_threshold': color_threshold,
                                   'button_threshold': button_threshold, 'template_path': template_path, 'wish': wish,
                                   'mode': mode, 'x_offset': x_offset, "y_offset": y_offset}
        with open(self.config_file, 'w') as file:
            self.config.write(file)

    def update_selection(self):
        self.selected_colors = [color for color, var in self.check_buttons if var.get() == 1]
        # print("Selected colors:", self.selected_colors)


class GUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FEH Helper")
        current_time = datetime.now()
        time_string = current_time.strftime("%Y-%m-%d-%H-%M-%S")
        self.log_name = "logs/" + time_string + ".txt"

        output_box = ttk.LabelFrame(self.root, text="Output_Box")
        output_box.pack()
        self.text = tk.Text(output_box, state=tk.DISABLED, width=60, height=20)
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(output_box)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text.yview)

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True)

        frame1 = ttk.Frame(notebook)
        frame2 = ttk.Frame(notebook)

        notebook.add(frame1, text='Story Passer')
        notebook.add(frame2, text='Wish Helper')

        f1 = RunningFrame(frame1, self.log_name)
        # f1 = RunningFrame(frame1)
        f2 = RunningFrame2(frame2, self.log_name)
        stop_button = tk.Button(self.root, text="Quit", command=self.root.destroy)
        stop_button.pack()

        self.root.after(100, self.update_text_widget)
        self.root.mainloop()

    def update_text_widget(self):

        try:
            with open(self.log_name, 'r', encoding='utf-8') as file:
                content = file.read()
                self.text.configure(state=tk.NORMAL)
                self.text.delete(1.0, tk.END)
                self.text.insert(tk.END, content)
                self.text.see(tk.END)
                self.text.configure(state=tk.DISABLED)
        except FileNotFoundError:
            self.text.configure(state=tk.NORMAL)
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, "File not found. Or script not started")
            self.text.see(tk.END)
            self.text.configure(state=tk.DISABLED)

        self.root.after(1000, self.update_text_widget)


if __name__ == '__main__':
    gui = GUI()
