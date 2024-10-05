# file_list_view.py
import os
import sys
import threading
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk  # Ensure customtkinter is installed
from PIL import Image, ImageTk

from widget.scrollable_frame import ScrollableFrame
from widget.underlined_frame import UnderlinedFrame
from util.event_bus import event_bus
from util.image_util import resize_image


class FileListView:
    def __init__(self, parent):
        self.entry_thread_id = None
        self.parent = parent
        self.file_list = []
        self.filtered_list = []
        self.path_cell_frames = []
        self.checkbox_vars = []
        self.notification_image_labels = []
        self.notification_txt_labels = []
        self.checkbox_checked_image = None
        self.checkbox_uncheck_image = None
        self.success_scaled_image = None
        self.error_scaled_image = None
        self.waiting_scaled_image = None
        self.balloon = None
        self.init_icons()

    def init_icons(self):
        try:
            # Load and resize images
            waiting_image = Image.open('res/icon/waiting.png')
            img = resize_image(waiting_image, (15, 15))
            self.waiting_scaled_image = ImageTk.PhotoImage(img)
            error_image = Image.open('res/icon/error.png')
            img = resize_image(error_image, (15, 15))
            self.error_scaled_image = ImageTk.PhotoImage(img)
            success_image = Image.open('res/icon/success.png')
            img = resize_image(success_image, (15, 15))
            self.success_scaled_image = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading notification icons: {e}")

    def create_widgets(self):
        # Scrollable Frame
        UnderlinedFrame(self.parent, padx=20)
        self.scrollable_frame = ScrollableFrame(self.parent)
        self.scrollable_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=20, pady=(0, 30), expand=True, anchor=tk.N)

    def update_file_list(self, file_list):
        self.file_list = file_list
        self.thread_filter_file()

    def clear_file_list(self):
        event_bus.publish("CloseTooltip", data=self.notification_txt_labels)
        for widget in self.path_cell_frames:
            widget.destroy()
        self.scrollable_frame.clean()
        self.path_cell_frames.clear()
        self.checkbox_vars.clear()
        self.notification_image_labels.clear()
        self.notification_txt_labels.clear()

    def add_file_entry(self, file_path):
        cell_frame = tk.Frame(self.scrollable_frame.scrollable_frame)
        cell_frame.pack(side=tk.TOP, anchor=tk.W, fill=tk.X, pady=(0, 0))
        cell_frame.config(highlightbackground='#E0E0E0', highlightcolor='gray', highlightthickness=1)
        # Checkbox variable
        var = tk.BooleanVar(value=True)
        self.checkbox_vars.append(var)
        # File path label
        file_path_label = tk.Label(cell_frame, text=file_path, cursor="hand2")
        file_path_label.pack(side=tk.LEFT, fill=tk.X, padx=(5, 0), pady=0, anchor=tk.W)
        file_path_label.bind("<Double-Button-1>", self.open_source_file)
        # Checkbox
        checkbox = ctk.CTkCheckBox(
            cell_frame,
            variable=var,
            text="",
            width=30,
            height=30,
            corner_radius=3,
            command=self.update_convert_button_state,
            fg_color="white",
            border_color="white",
            border_width=3,
            bg_color="white",
            hover_color="white",
            checkmark_color="gray",
        )
        checkbox.pack(side=tk.RIGHT, padx=(0, 0), pady=0, anchor=tk.E)
        # Notification Image Label
        image_label = tk.Label(cell_frame, image=self.waiting_scaled_image)
        image_label.pack(side=tk.RIGHT, padx=(10, 10), pady=0)
        self.notification_image_labels.append(image_label)
        # Notification Text Label
        txt_label = tk.Label(cell_frame)
        txt_label.pack(side=tk.RIGHT, padx=(10, 10), pady=0)
        self.notification_txt_labels.append(txt_label)
        self.path_cell_frames.append(cell_frame)

    def open_source_file(self, event):
        label = event.widget
        file_path = label.cget("text")
        if os.path.exists(file_path):
            try:
                if os.name == 'nt':  # For Windows
                    os.startfile(file_path, 'open')
                elif os.name == 'posix':  # For macOS and Linux
                    import subprocess
                    subprocess.call(('open' if sys.platform == 'darwin' else 'xdg-open', file_path))
                else:
                    messagebox.showerror("错误", "不支持的操作系统。")
            except Exception as e:
                messagebox.showerror("错误", f"无法打开文件:\n{e}")
        else:
            messagebox.showwarning("警告", "文件路径不存在！")

    def update_convert_button_state(self):
        # Implement logic to enable/disable the convert button based on checkbox states
        any_checked = any(var.get() for var in self.checkbox_vars)
        if any_checked:
            self.parent.conversion_manager.enable_convert_button_when_disable()
        else:
            self.parent.conversion_manager.disable_convert_button_when_enable()

    def thread_filter_file(self, event=None):
        self.clear_file_list()
        # Implement the filtering logic based on selected filters
        threading.Thread(target=self.filter_file_by_filter_source_and_except_filter_source).start()

    def filter_file_by_filter_source_and_except_filter_source(self):
        # set entry thread_id for the before thread compare
        self.entry_thread_id = threading.get_ident()
        self.parent.conversion_manager.reset_convert_button_and_progress_bar()
        include_filters = self.parent.filter_options.get_filters()["include"]
        exclude_filters = self.parent.filter_options.get_filters()["exclude"]
        filtered_list = self.filter_file_by_search(self.file_list)
        filtered_list = self.filter_file_by_include(filtered_list, include_filters)
        filtered_list = self.filter_file_by_exclude(filtered_list, exclude_filters)
        self.display_filtered_files(filtered_list)

    def filter_file_by_search(self, file_list):
        search_input = self.parent.search_filter_options.search_input_entry_text.get()
        if search_input:
            return [file for file in file_list if search_input.lower() in file.lower()]
        return file_list

    def filter_file_by_include(self, file_list, include_filters):
        if not include_filters:
            return file_list
        return [file for file in file_list if any(file.endswith(ext) for ext in include_filters)]

    def filter_file_by_exclude(self, file_list, exclude_filters):
        if not exclude_filters:
            return file_list
        return [file for file in file_list if not any(file.endswith(ext) for ext in exclude_filters)]

    def display_filtered_files(self, filtered_list):
        self.filtered_list = filtered_list
        self.parent.progress_manager.progress_bar.set_total_count(len(filtered_list))
        for path in filtered_list:
            current_thread_id = threading.get_ident()
            self.add_file_entry(path)
            # stop the other thread
            if not current_thread_id == self.entry_thread_id:
                return
            self.parent.progress_manager.progress_bar.go_forward(1)
        # Update the "Select All" checkbox based on whether all items are selected
        self.parent.search_filter_options.select_all_checkbox.set_state(all(var.get() for var in self.checkbox_vars))
        if any(var.get() for var in self.checkbox_vars):
            self.parent.conversion_manager.enable_convert_button()
        else:
            self.parent.conversion_manager.disable_convert_button()
