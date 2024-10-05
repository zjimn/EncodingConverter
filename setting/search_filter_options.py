# filter_options.py
import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk

from widget.icon_checkbox import IconCheckbox
from util.event_bus import event_bus
from util.image_util import resize_image


class SearchFilterOptions:
    def __init__(self, parent):
        self.filter_icon = None
        self.parent = parent
        self.filter_source_dropdown = None
        self.except_filter_source_dropdown = None
        self.select_all_checkbox = None
        self.select_all_label = None
        self.search_input_entry_text = None
        self.search_input_entry = None

    def create_widgets(self, frame):
        # Bottom Frame for Search and Select All
        filter_bottom_frame = ttk.Frame(frame)
        filter_bottom_frame.pack(side=tk.TOP, fill=tk.X, anchor=tk.N)
        # Search Input Frame
        filter_search_frame = tk.Frame(filter_bottom_frame, bg='gray', bd=1)
        filter_search_frame.pack(side=tk.LEFT, anchor=tk.CENTER, fill=tk.X, expand=True, padx=(0, 10))
        filter_search_frame.config(highlightbackground='#E0E0E0', highlightcolor='gray', highlightthickness=0)
        # Optional: Add a search icon
        try:
            filter_image = Image.open('res/icon/filter.png')
            icon_image = resize_image(filter_image, (20, 20))
            self.filter_icon = ImageTk.PhotoImage(icon_image)
            image_label = tk.Label(filter_search_frame, image=self.filter_icon, bg='gray')
            image_label.pack(side=tk.LEFT, padx=(0, 5))
        except Exception as e:
            print(f"Failed to load search icon: {e}")
        self.search_input_entry_text = tk.StringVar()
        self.search_input_entry = ttk.Entry(filter_search_frame, textvariable=self.search_input_entry_text, width=50)
        self.search_input_entry.pack(side=tk.LEFT, fill=tk.X, pady=5, anchor=tk.N)
        self.search_input_entry.config(cursor="xterm")  # Optional: Change cursor to indicate it's editable
        # Bind search input to trigger filtering
        self.search_input_entry_text.trace_add('write', self.on_search_input_change)
        # Select All Checkbox
        self.select_all_checkbox = IconCheckbox(filter_bottom_frame)
        self.select_all_checkbox.pack(side=tk.RIGHT, padx=(0, 0), pady=0)  # Adjust padding as needed
        self.select_all_checkbox.set_enabled(False)
        self.select_all_label = tk.Label(filter_bottom_frame, text="全选", width=0)
        self.select_all_label.pack(side=tk.RIGHT, padx=(0, 5), pady=10)
        self.select_all_checkbox.bind("<<CheckboxToggled>>", self.toggle_select_all)
        event_bus.subscribe("ReadyConvert", self.on_ready_convert)
        event_bus.subscribe("DisableConvert", self.on_disable_convert)

    def on_disable_convert(self, *args):
        # Trigger filtering when search input changes
        self.select_all_checkbox.set_enabled(False)

    def on_ready_convert(self, *args):
        # Trigger filtering when search input changes
        self.select_all_checkbox.set_enabled(True)

    def on_search_input_change(self, *args):
        # Trigger filtering when search input changes
        self.parent.file_list_view.thread_filter_file()

    def toggle_select_all(self, event):
        all_selected = self.select_all_checkbox.get_state()
        if all_selected:
            # Select all checkboxes
            for var in self.parent.file_list_view.checkbox_vars:
                var.set(True)
        else:
            # Deselect all checkboxes
            for var in self.parent.file_list_view.checkbox_vars:
                var.set(False)
        # Update the convert button state
        self.parent.file_list_view.update_convert_button_state()
