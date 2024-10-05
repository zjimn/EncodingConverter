# filter_options.py
import tkinter as tk
from tkinter import ttk

from widget.multi_select_dropdown import MultiSelectDropdown


class FilterOptions:
    def __init__(self, parent):
        self.filter_icon = None
        self.parent = parent
        self.filter_source_dropdown = None
        self.except_filter_source_dropdown = None
        self.select_all_checkbox = None
        self.select_all_label = None

    def create_widgets(self, frame):
        # Top Frame for Filters
        filter_top_frame = ttk.Frame(frame)
        filter_top_frame.pack(side=tk.TOP, fill=tk.X, anchor=tk.N)
        # filter files
        filter_file_label = tk.Label(filter_top_frame, text="过滤文件:")
        filter_file_label.pack(side=tk.LEFT, padx=(0, 5), pady=10)
        self.filter_source_dropdown = MultiSelectDropdown(filter_top_frame, self.parent)
        self.filter_source_dropdown.pack(side=tk.LEFT, padx=(0, 10), pady=10, fill=tk.X, expand=True)
        # exclude files
        except_filter_file_label = tk.Label(filter_top_frame, text="排除文件:")
        except_filter_file_label.pack(side=tk.LEFT, padx=(10, 5), pady=10)
        self.except_filter_source_dropdown = MultiSelectDropdown(filter_top_frame, self.parent)
        self.except_filter_source_dropdown.pack(side=tk.LEFT, padx=(0, 0), pady=10, fill=tk.X, expand=True)
        # bind events to trigger filtering
        self.filter_source_dropdown.entry.bind("<<EntryUpdated>>", self.parent.file_list_view.thread_filter_file)
        self.except_filter_source_dropdown.entry.bind("<<EntryUpdated>>", self.parent.file_list_view.thread_filter_file)

    def on_search_input_change(self, *args):
        # Trigger filtering when search input changes
        self.parent.file_list_view.thread_filter_file()

    def get_filters(self):
        return {
            "include": self.filter_source_dropdown.get_selected_list(),
            "exclude": self.except_filter_source_dropdown.get_selected_list()
        }
