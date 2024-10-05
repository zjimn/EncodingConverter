# conversion_manager.py
import os
import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from ttkbootstrap import Style

from util.char_util import detect_encoding
from util.event_bus import event_bus


class ButtonState:
    WAITING = 0
    LOADING = 1
    DISABLED = 2
    ENABLED = 3
    CONVERTING = 4
    FINISHED = 5


class ConversionManager:
    def __init__(self, parent):
        self.parent = parent
        self.convert_button = None
        self.button_state = ButtonState.LOADING
        self.style = Style(theme='litera')
        self.init_style()

    def init_style(self):
        self.style.configure(
            'Custom.TCheckbutton',
            font=('Helvetica', 80),
            padding=5
        )
        self.style.configure("Waiting.TButton",
                             foreground="white",
                             background="#e8590c",
                             padding=8,
                             borderwidth=0)
        self.style.configure("Ready.TButton",
                             foreground="white",
                             background="#e8590c",
                             padding=8,
                             borderwidth=0,
                             highlightbackground="#e8590c",
                             highlightcolor="#fc6d20")
        self.style.map("Ready.TButton",
                       foreground=[('active', 'white'), ('disabled', '#c5c4c7')],
                       background=[('active', '#fc6d20'), ('disabled', '#eaebeb')])
        self.style.configure("Loading.TButton",
                             foreground="white",
                             background="#4582ec",
                             padding=8,
                             borderwidth=0,
                             highlightbackground="#4582ec",
                             highlightcolor="#4582ec")
        self.style.map("Loading.TButton",
                       foreground=[('disabled', 'white')],
                       background=[('disabled', '#4582ec')])
        self.style.configure("Clicked.TButton",
                             foreground="white",
                             background="#4582ec",
                             padding=8,
                             borderwidth=0,
                             highlightbackground="red",
                             highlightcolor="red")
        self.style.map("Clicked.TButton",
                       foreground=[('disabled', 'white')],
                       background=[('disabled', 'red')])
        self.style.configure("ConvertFinished.TButton",
                             foreground="white",
                             background="#4582ec",
                             padding=8,
                             borderwidth=0,
                             highlightbackground="green",
                             highlightcolor="green")
        self.style.map("ConvertFinished.TButton",
                       foreground=[('disabled', 'white')],
                       background=[('disabled', 'green')])

    def create_widgets(self, frame):
        self.convert_button = ttk.Button(
            frame,
            text="等待加载",
            command=self.threading_convert_files,
            style="Custom.TButton",
            state='disabled'
        )
        self.convert_button.pack(side=tk.RIGHT, pady=0)
        self.update_button_state(ButtonState.WAITING)

    def threading_convert_files(self):
        threading.Thread(target=self.convert_files).start()

    def convert_files(self):
        self.parent.conversion_manager.reset_convert_button_and_progress_bar()
        self.update_button_state(ButtonState.CONVERTING)
        encodings = self.parent.encoding_options.get_encodings()
        file_paths = self.parent.file_list_view.filtered_list
        total_files = len(file_paths)
        self.parent.progress_manager.progress_bar.set_total_count(total_files)
        self.parent.progress_manager.progress_bar.current_count = 0  # Reset progress
        for index, file_path in enumerate(file_paths):
            if not self.parent.file_list_view.checkbox_vars[index].get():
                continue  # Skip unchecked files
            image_label = self.parent.file_list_view.notification_image_labels[index]
            txt_label = self.parent.file_list_view.notification_txt_labels[index]
            tip = ""
            try:
                self.convert_encoding(file_path, encodings)
                image_label.configure(image=self.parent.file_list_view.success_scaled_image)
            except UnicodeDecodeError as e:
                print(e)
                tip = e.reason
                image_label.configure(image=self.parent.file_list_view.error_scaled_image)
            except Exception as e:
                print(e)
                tip = e
                image_label.configure(image=self.parent.file_list_view.error_scaled_image)
            finally:
                self.parent.progress_manager.progress_bar.go_forward(1)
            event_bus.publish("ShowTooltip", data=(image_label, tip))
            txt_label.configure(text=f"{encodings['source']} -> {encodings['target']}")
        self.update_button_state(ButtonState.FINISHED)
        self.parent.focus_set()
        messagebox.showinfo("成功", "文件转换完成！")

    def convert_encoding(self, input_file, encodings):
        # Auto-detect source encoding if needed
        source_encoding = encodings["source"]
        target_encoding = encodings["target"]
        if source_encoding == "自动识别":
            source_encoding = detect_encoding(input_file)
            encodings["source"] = source_encoding
        with open(input_file, 'r', encoding=source_encoding) as f:
            content = f.read()
        with open(input_file, 'w', encoding=target_encoding) as f:
            f.write(content)

    def process_directory(self, directory, target_encoding, source_encoding):
        """Recursively process all files in the directory"""
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                encodings = {"source": source_encoding, "target": target_encoding}
                try:
                    self.convert_encoding(file_path, encodings)
                    print(f"转换文件: {file_path} 到 {target_encoding}")
                except Exception as e:
                    print(f"处理文件 {file_path} 时出错：{e}")

    def update_button_state(self, state):
        publish_select_all_event = False
        if state == ButtonState.WAITING:
            self.convert_button.configure(state='disabled', text="等待加载")
            self.convert_button.configure(style="Waiting.TButton")
        if state == ButtonState.LOADING:
            self.convert_button.configure(state='disabled', text="正在加载")
            self.convert_button.configure(style="Loading.TButton")
        if state == ButtonState.DISABLED:
            self.convert_button.configure(state='disabled', text="开始转换")
            self.convert_button.configure(style="Ready.TButton")
            self.convert_button.state(['disabled'])
            publish_select_all_event = True
        elif state == ButtonState.ENABLED:
            self.convert_button.configure(state='normal', text="开始转换")
            self.convert_button.configure(style="Ready.TButton")
            publish_select_all_event = True
        elif state == ButtonState.CONVERTING:
            self.convert_button.configure(style="Clicked.TButton")
            self.convert_button.configure(state='disabled', text="正在转换")
        elif state == ButtonState.FINISHED:
            self.convert_button.configure(state='disabled', text="转换完成")
            self.convert_button.configure(style="ConvertFinished.TButton")
            publish_select_all_event = True
        if publish_select_all_event:
            event_bus.publish("ReadyConvert")
        else:
            event_bus.publish("DisableConvert")
        self.button_state = state

    def disable_convert_button(self):
        self.update_button_state(ButtonState.DISABLED)

    def enable_convert_button(self):
        self.update_button_state(ButtonState.ENABLED)

    def enable_convert_button_when_disable(self):
        if self.button_state == ButtonState.DISABLED:
            self.update_button_state(ButtonState.ENABLED)

    def disable_convert_button_when_enable(self):
        if self.button_state == ButtonState.ENABLED:
            self.update_button_state(ButtonState.DISABLED)

    def reset_convert_button_and_progress_bar(self):
        self.convert_button.configure(text="正在加载")
        self.convert_button.configure(style="Loading.TButton")
        self.convert_button.configure(state='disabled')
        self.button_state = ButtonState.LOADING
        if self.parent.progress_manager.progress_bar:
            self.parent.progress_manager.progress_bar.clean()

    def update_select_all_checkbox_state(self):
        # Update the state of the "select all" checkbox based on individual selections
        all_selected = all(var.get() for var in self.parent.file_list_view.checkbox_vars)
        any_selected = any(var.get() for var in self.parent.file_list_view.checkbox_vars)
        if all_selected and any_selected:
            self.parent.filter_options.select_all_checkbox.set_state(True)
        elif not any_selected:
            self.parent.filter_options.select_all_checkbox.set_state(False)
        else:
            self.parent.filter_options.select_all_checkbox.set_state(False)
