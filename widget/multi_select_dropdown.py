import tkinter as tk
from tkinter import ttk


class MultiSelectDropdown:
    def __init__(self, master, root):
        self.master = master
        self.entry_text = tk.StringVar()
        self.entry = ttk.Entry(master, textvariable=self.entry_text)
        self.entry.pack(side=tk.LEFT, padx=0, pady=10, fill=tk.X, expand=True)
        self.listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, height=5)
        self.options = [".txt", ".md", ".rtf", ".csv", ".html", ".css", ".js", ".json", ".xml", ".yaml", ".yml",
                        ".py", ".java", ".c", ".cpp", ".cs", ".bat", ".sh", ".ini", ".log", ".tex"]
        for option in self.options:
            self.listbox.insert(tk.END, option)
        self.entry.bind("<Button-1>", self.show_listbox)
        self.entry.bind("<Leave>", self.check_leave_entry)
        self.listbox.bind("<Leave>", self.hide_listbox)
        self.listbox.bind("<<ListboxSelect>>", self.update_entry)
        self.entry_text.trace_add('write', self.update_input_entry)
        self.update_event_timer = None

    def get_selected_list(self):
        if not self.entry or self.entry.get() == "":
            return []
        return self.entry.get().split(", ")

    def show_listbox(self, event):
        current_selection = self.entry.get().split(", ")
        if current_selection:
            self.listbox.selection_clear(0, tk.END)
            for item in current_selection:
                if item in self.options:
                    index = self.options.index(item)
                    self.listbox.selection_set(index)
        self.listbox.place(x=self.entry.winfo_x() + 407, y=self.entry.winfo_y() + self.entry.winfo_height() + 80)

    def check_leave_entry(self, event):
        mouse_x = event.x_root
        mouse_y = event.y_root
        listbox_x = self.listbox.winfo_rootx()
        listbox_y = self.listbox.winfo_rooty()
        listbox_width = self.listbox.winfo_width()
        listbox_height = self.listbox.winfo_height()
        # determine whether the mouse is in the listbox area
        if not (listbox_x <= mouse_x <= listbox_x + listbox_width and
                listbox_y <= mouse_y <= listbox_y + listbox_height):
            self.hide_listbox()

    def hide_listbox(self, event=None):
        self.listbox.place_forget()

    def hide_listbox_on_click_outside(self, event):
        x, y = event.x, event.y
        entry_x = self.entry.winfo_x()
        entry_y = self.entry.winfo_y()
        entry_height = self.entry.winfo_height()
        listbox_height = self.listbox.winfo_height()
        # determine whether the mouse is outside the listbox area
        if not (entry_x <= x <= entry_x + self.entry.winfo_width() and entry_y <= y <= entry_y + entry_height) and \
                not (
                        entry_x <= x <= entry_x + self.entry.winfo_width() and entry_y + entry_height <= y <= entry_y + entry_height + listbox_height):
            self.hide_listbox()

    def update_entry(self, *args):
        if not self.listbox.place_info():
            return
        selected_indices = self.listbox.curselection()
        selected_items = [self.listbox.get(i) for i in selected_indices]
        self.entry.delete(0, tk.END)
        self.entry.insert(0, ", ".join(selected_items))
        if self.update_event_timer:
            self.entry.after_cancel(self.update_event_timer)
        self.update_event_timer = self.entry.after(0, self.trigger_entry_updated)
        self.hide_listbox()

    # avoid frequent trigger
    def update_input_entry(self, *args):
        if self.update_event_timer:
            self.entry.after_cancel(self.update_event_timer)
        self.update_event_timer = self.entry.after(0, self.trigger_entry_updated)

    def get_content(self):
        return self.entry.get()

    def trigger_entry_updated(self):
        self.entry.event_generate("<<EntryUpdated>>")
        self.update_event_timer = None

    def pack(self, **kwargs):
        self.entry.pack(**kwargs)


if __name__ == "__main__":
    root = tk.Tk()
    dropdown = MultiSelectDropdown(root, root)
    root.mainloop()
