# filter_options.py
import tkinter as tk
from tkinter import ttk

from manager.LanguageManager import LanguageManager
from util.event_bus import event_bus
from widget.multi_select_dropdown import MultiSelectDropdown


class FilterOptions(LanguageManager):
    def __init__(self, parent):
        super().__init__()
        self.previous_x = None
        self.previous_y = None
        self.previous_height = None
        self.previous_width = None
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
        filter_file_label = tk.Label(filter_top_frame, text=self._("Filter File:"))
        filter_file_label.pack(side=tk.LEFT, padx=(0, 5), pady=10)
        self.filter_source_dropdown = MultiSelectDropdown(filter_top_frame, self.parent)
        self.filter_source_dropdown.pack(side=tk.LEFT, padx=(0, 10), pady=10, fill=tk.X, expand=True)
        # exclude files
        except_filter_file_label = tk.Label(filter_top_frame, text=self._("Except File:"))
        except_filter_file_label.pack(side=tk.LEFT, padx=(10, 5), pady=10)
        self.except_filter_source_dropdown = MultiSelectDropdown(filter_top_frame, self.parent)
        self.except_filter_source_dropdown.pack(side=tk.LEFT, padx=(0, 0), pady=10, fill=tk.X, expand=True)
        # bind events to trigger filtering
        self.filter_source_dropdown.entry.bind("<<EntryUpdated>>", self.parent.file_list_view.thread_filter_file)
        self.except_filter_source_dropdown.entry.bind("<<EntryUpdated>>", self.parent.file_list_view.thread_filter_file)
        self.parent.bind_all("<Configure>", self.on_configure)

    def on_search_input_change(self, *args):
        # Trigger filtering when search input changes
        self.parent.file_list_view.thread_filter_file()

    def get_filters(self):
        return {
            "include": self.filter_source_dropdown.get_selected_list(),
            "exclude": self.except_filter_source_dropdown.get_selected_list()
        }

    def on_configure(self, event):
        if event.widget == self.parent:
            check = False
            if (event.width != self.previous_width) or (event.height != self.previous_height):
                self.previous_width = event.width
                self.previous_height = event.height
                check = True
            elif (event.x != self.previous_x) or (event.y != self.previous_y):
                self.previous_x = event.x
                self.previous_y = event.y
                check = True

            if check:
                event_bus.publish("UpdateMainWindow")