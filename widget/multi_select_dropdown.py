import tkinter as tk
from tkinter import ttk

from util.event_bus import event_bus


class MultiSelectDropdown:
    def __init__(self, master, root):
        self.listbox_window = None
        self.listbox = None
        self.master = master
        self.root = root
        self.entry_text = tk.StringVar()

        # 创建 Entry 小部件
        self.entry = ttk.Entry(master, textvariable=self.entry_text)
        self.entry.pack(side=tk.LEFT, padx=0, pady=10, fill=tk.X, expand=True)

        # 初始化选项
        self.options = [".txt", ".md", ".rtf", ".csv", ".html", ".css", ".js", ".json",
                        ".xml", ".yaml", ".yml", ".py", ".java", ".c", ".cpp",
                        ".cs", ".bat", ".sh", ".ini", ".log", ".tex"]

        # 绑定事件
        self.entry.bind("<Button-1>", self.show_listbox)
        self.entry.bind("<FocusOut>", self.on_focus_out)
        self.entry_text.trace_add('write', self.update_input_entry)
        event_bus.subscribe("UpdateMainWindow", self.hide_listbox)
        self.update_event_timer = None
        self.create_listbox_window()


    def create_listbox_window(self):
        # 创建一个新的 Toplevel 窗口
        self.listbox_window = tk.Toplevel(self.master)
        self.listbox_window.withdraw()  # 初始时隐藏
        self.listbox_window.overrideredirect(True)  # 去掉窗口边框
        self.listbox_window.attributes("-topmost", True)  # 窗口置顶

        # 创建 Listbox
        self.listbox = tk.Listbox(self.listbox_window, selectmode=tk.MULTIPLE, height=5)
        self.listbox.pack(fill=tk.X, expand=True)

        # 插入选项
        for option in self.options:
            self.listbox.insert(tk.END, option)

        # 绑定 Listbox 事件
        self.listbox.bind("<<ListboxSelect>>", self.update_entry)

        # 绑定点击窗口外部以隐藏 Listbox
        self.master.bind_all("<Button-1>", self.on_click_outside, "+")

    def show_listbox(self, event):
        # 更新 Listbox 的选中状态
        current_selection = self.get_selected_list()
        self.listbox.selection_clear(0, tk.END)
        for item in current_selection:
            if item in self.options:
                index = self.options.index(item)
                self.listbox.selection_set(index)


        required_height = 5 * 20

        # 获取 Entry 的绝对位置
        self.master.update_idletasks()  # 确保位置准确
        x = self.entry.winfo_rootx()
        y = self.entry.winfo_rooty() + self.entry.winfo_height()
        width = self.entry.winfo_width()

        # 设置 Listbox 窗口的位置和宽度
        self.listbox_window.geometry(f"{width}x{required_height}+{x}+{y}")
        self.listbox_window.deiconify()  # 显示窗口
        self.listbox.pack(fill=tk.X, expand=True)

    def hide_listbox(self, *args):
        self.root.after(0, self.listbox_window.withdraw)

    def on_click_outside(self, event):
        widget = event.widget
        if widget != self.entry and widget != self.listbox:
            self.hide_listbox()

    def on_focus_out(self, event):
        self.hide_listbox()



    def update_entry(self, *args):
        if self.listbox_window is None or not self.listbox_window.winfo_viewable():
            return
        selected_indices = self.listbox.curselection()
        selected_items = [self.listbox.get(i) for i in selected_indices]
        self.entry.delete(0, tk.END)
        self.entry.insert(0, ", ".join(selected_items))
        if self.update_event_timer:
            self.entry.after_cancel(self.update_event_timer)
        self.update_event_timer = self.entry.after(0, self.trigger_entry_updated)
        self.hide_listbox()

    def update_input_entry(self, *args):
        if self.update_event_timer:
            self.master.after_cancel(self.update_event_timer)
        self.update_event_timer = self.master.after(300, self.trigger_entry_updated)


    def get_selected_list(self):
        text = self.entry.get()
        if not text:
            return []
        return [item.strip() for item in text.split(",")]

    def trigger_entry_updated(self):
        self.entry.event_generate("<<EntryUpdated>>")
        self.update_event_timer = None

    def pack(self, **kwargs):
        self.entry.pack(**kwargs)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x300")
    dropdown = MultiSelectDropdown(root, root)
    root.mainloop()
