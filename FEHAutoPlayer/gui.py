import multiprocessing
import sys
import tkinter as tk
# from threading import Thread, Event
from tkinter import ttk
import time


import story_passer
class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, string):
        self.widget.insert(tk.END, string)

    def flush(self):
        pass  # necessary for file-like objects

class RunningFrame(tk.Frame):

    def __init__(self,i_frame, master=None, **kwargs):

        super().__init__(master, **kwargs)
        # self.pack()

        #
        # output_box = ttk.LabelFrame(self, text="Output_Box")
        # self.text = tk.Text(output_box, width=60, height=30)
        # self.text.grid(row=1, column=0, padx=10, pady=10)
        # sys.stdout = TextRedirector(self.text)
        # output_box.grid(row=0, column=0, padx=10, pady=10)

        input_area = ttk.LabelFrame(i_frame, text="Input_Area")
        input_area.grid(row=1, column=0, padx=10, pady=10)
        window_name_label = tk.Label(input_area, text="window_name:")
        window_name_label.grid(row=0, column=0, padx=10, pady=10)
        window_name_entry = tk.Entry(input_area, width=50)
        window_name_entry.grid(row=0, column=1, padx=10, pady=10)

        # Create a label for the template path and a text entry field
        template_path_label = tk.Label(input_area, text="template_path:")
        template_path_label.grid(row=1, column=0, padx=10, pady=10)
        template_path_entry = tk.Entry(input_area, width=50)
        template_path_entry.grid(row=1, column=1, padx=10, pady=10, columnspan=3)

        label = tk.Label(input_area, text="Thresholds :")
        label.grid(row=3, column=0, padx=10, pady=10)

        # Create a scale (slider) for values between 0 and 1
        slider = tk.Scale(input_area, from_=0, to=1, resolution=0.01, orient="horizontal", command="")
        slider.grid(row=3, column=1, padx=10, pady=10)

        start_button = tk.Button(input_area, text="Start", command=self.start)
        start_button.grid(row=4, column=0, padx=10, pady=10)

        stop_button = tk.Button(input_area, text="Stop", command=self.stop)
        stop_button.grid(row=4, column=1, padx=10, pady=10)

        self.stop_event = multiprocessing.Event()
        self.process = None

    def start(self):
        if self.process is not None and self.process.is_alive():
            return

        self.stop_event.clear()

        self.process = multiprocessing.Process(target=self.run_loop)
        self.process.start()

    def stop(self):
        if self.process is not None and self.process.is_alive():
            self.stop_event.set()
            self.process.join()

    def run_loop(self):
        while not self.stop_event.is_set():
            story_passer.execute("_hard", 'MuMu模拟器12')


def run_gui():
    root = tk.Tk()

    output_box = ttk.LabelFrame(root, text="Output_Box")
    text = tk.Text(output_box, width=60, height=30)
    text.pack()
    sys.stdout = TextRedirector(text)
    output_box.pack()
    sys.stdout = TextRedirector(text)

    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)

    frame1 = ttk.Frame(notebook)
    frame2 = ttk.Frame(notebook)

    notebook.add(frame1, text='Story Passer')
    notebook.add(frame2, text='Wish Helper')

    f1 = RunningFrame(frame1)
    f2 = RunningFrame(frame2)

    root.mainloop()

if __name__ == '__main__':
    run_gui()