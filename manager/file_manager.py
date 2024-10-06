# file_manager.py
import tkinter as tk
from pathlib import Path
from tkinter import filedialog
from tkinter import ttk

from manager.LanguageManager import LanguageManager


class FileManager(LanguageManager):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.path_entry = None
        self.file_list = []

    def create_widgets(self, frame):
        self.path_entry = ttk.Entry(frame, state='readonly')
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, padx=(0, 10), pady=10, expand=True)
        self.path_entry.config(cursor="arrow")
        browse_file_btn = ttk.Button(frame, text=self._("Select File"), command=self.select_files)
        browse_file_btn.pack(side=tk.LEFT, padx=10, pady=10)
        browse_dir_btn = ttk.Button(frame, text=self._("Select Directory"), command=self.select_directory)
        browse_dir_btn.pack(side=tk.LEFT, padx=(10, 0), pady=10)

    def select_files(self):
        file_paths = filedialog.askopenfilenames()
        if file_paths:
            self.update_path_entry(file_paths)
            self.file_list = list(file_paths)
            self.parent.file_list_view.update_file_list(self.file_list)

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.update_path_entry([directory])
            self.file_list = self.list_files_in_directory(directory)
            self.parent.file_list_view.update_file_list(self.file_list)

    def update_path_entry(self, paths):
        self.path_entry.config(state='normal')
        self.path_entry.delete(0, tk.END)
        if len(paths) == 1:
            self.path_entry.insert(0, paths[0])
        else:
            self.path_entry.insert(0, "\n".join(paths))
        self.path_entry.config(state='readonly')

    def list_files_in_directory(self, directory):
        file_paths = []
        p = Path(directory)
        for file in p.rglob('*'):
            if file.is_file():
                file_paths.append(file.resolve().as_posix())
        return file_paths
