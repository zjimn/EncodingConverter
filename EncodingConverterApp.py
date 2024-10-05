# encoding_converter_app.py
import tkinter as tk
from tkinter import ttk

from ttkbootstrap import Style

from manager.conversion_manager import ConversionManager
from setting.encoding_options import EncodingOptions
from view.file_list_view import FileListView
from manager.file_manager import FileManager
from setting.filter_options import FilterOptions
from setting.search_filter_options import SearchFilterOptions
from widget.tooltip import Tooltip
from util.event_bus import event_bus
from util.window_util import center_window
from manager.progress_manager import ProgressManager


class EncodingConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("encoding convert tool")
        self.geometry("1000x620")
        center_window(self, 1000, 620)
        # Initialize styles
        self.style = Style(theme='litera')
        # Initialize components
        self.file_manager = FileManager(self)
        self.encoding_options = EncodingOptions(self)
        self.filter_options = FilterOptions(self)
        self.search_filter_options = SearchFilterOptions(self)
        self.file_list_view = FileListView(self)
        self.progress_manager = ProgressManager(self)
        self.conversion_manager = ConversionManager(self)
        # Initialize Tooltip
        self.tooltip = Tooltip(self)
        event_bus.subscribe("ShowTooltip", self.tooltip.bind)
        event_bus.subscribe("CloseTooltip", self.tooltip.unbind)
        # Create Main Container Frame
        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.BOTH)
        self.layout_components(main_container)

    def layout_components(self, parent):
        # Top Frame for File Selection
        top_frame = ttk.Frame(parent)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=20, pady=(20, 0), anchor=tk.N)
        self.file_manager.create_widgets(top_frame)
        # encoding options frame
        encoding_and_filter_frame = ttk.Frame(parent)
        encoding_and_filter_frame.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10, anchor=tk.N)
        # encoding options frame
        encoding_frame = ttk.Frame(encoding_and_filter_frame)
        encoding_frame.pack(side=tk.LEFT, fill=tk.X, padx=0, pady=0, anchor=tk.N)
        self.encoding_options.create_widgets(encoding_frame)
        # filter options frame
        filter_frame = ttk.Frame(encoding_and_filter_frame)
        filter_frame.pack(side=tk.LEFT, fill=tk.X, padx=0, pady=0, expand=True, anchor=tk.N)
        self.filter_options.create_widgets(filter_frame)
        # progress and convert button
        convert_frame = ttk.Frame(parent)
        convert_frame.pack(side=tk.TOP, fill=tk.X, anchor=tk.N, padx=20, pady=0)
        self.progress_manager.create_widgets(convert_frame)
        self.conversion_manager.create_widgets(convert_frame)
        # search filter options frame
        search_filter_frame = ttk.Frame(parent)
        search_filter_frame.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10, anchor=tk.N)
        self.search_filter_options.create_widgets(search_filter_frame)
        # file list view
        self.file_list_view.create_widgets()


if __name__ == "__main__":
    app = EncodingConverterApp()
    app.mainloop()
