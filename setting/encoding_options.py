# encoding_options.py
import tkinter as tk
from tkinter import ttk

from manager.LanguageManager import LanguageManager


class EncodingOptions(LanguageManager):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.source_encoding_var = tk.StringVar(value=self._("Auto Detect"))
        self.target_encoding_var = tk.StringVar(value="UTF-8")
        self.SOURCE_ENCODINGS = [self._("Auto Detect"), "UTF-8", "ASCII", "ISO-8859-1", "Windows-1252", "GBK", "GB18030", "ISO-8859-2",
                            "ISO-8859-3",
                            "ISO-8859-4", "Windows-1250", "Windows-1251", "UTF-16", "UTF-32", "Big5", "Shift JIS",
                            "EUC-JP",
                            "EUC-KR", "EUC-CN", "MacRoman", "ISO-2022-JP", "KOI8-R"]

        self.TARGET_ENCODINGS = ["UTF-8", "ASCII", "ISO-8859-1", "Windows-1252", "GBK", "GB18030", "ISO-8859-2",
                            "ISO-8859-3",
                            "ISO-8859-4", "Windows-1250", "Windows-1251", "UTF-16", "UTF-32", "Big5", "Shift JIS",
                            "EUC-JP",
                            "EUC-KR", "EUC-CN", "MacRoman", "ISO-2022-JP", "KOI8-R"]

    def create_widgets(self, frame):
        # Source Encoding Dropdown
        source_label = tk.Label(frame, text=self._("Source Encoding:"))
        source_label.pack(side=tk.LEFT, padx=(0, 5), pady=10)
        source_dropdown = ttk.Combobox(frame, textvariable=self.source_encoding_var,
                                       values=self.SOURCE_ENCODINGS, width=14, state="readonly")
        source_dropdown.pack(side=tk.LEFT, padx=(0, 10), pady=10)
        # Target Encoding Dropdown
        target_label = tk.Label(frame, text=self._("Target Encoding:"))
        target_label.pack(side=tk.LEFT, padx=(0, 5), pady=10)
        target_dropdown = ttk.Combobox(frame, textvariable=self.target_encoding_var,
                                       values=self.TARGET_ENCODINGS, width=14, state="readonly")
        target_dropdown.pack(side=tk.LEFT, padx=(0, 15), pady=10)
        source_dropdown.bind("<<ComboboxSelected>>", self.on_source_selected)
        target_dropdown.bind("<<ComboboxSelected>>", self.on_target_selected)

    # clear the bg after select
    def on_source_selected(self, event):
        value = self.source_encoding_var.get()
        self.source_encoding_var.set("")
        self.source_encoding_var.set(value)

    def on_target_selected(self, event):
        value = self.target_encoding_var.get()
        self.target_encoding_var.set("")
        self.target_encoding_var.set(value)

    def get_encodings(self):
        return {
            "source": self.source_encoding_var.get(),
            "target": self.target_encoding_var.get()
        }
