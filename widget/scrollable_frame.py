import tkinter as tk
from tkinter import ttk


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, borderwidth=0, relief=tk.RAISED)
        self.window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.container = container
        self.container.bind("<Configure>", lambda e: self.update_scroll_region())
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.scrollbar_visible = False
        self.scrollbar.pack_forget()
        self.bind("<Configure>", self.on_resize)
        self.container.bind("<MouseWheel>", self.on_mouse_wheel)

    def on_mouse_wheel(self, event):
        # Check if the mouse is inside the scrollable_frame
        x, y = self.winfo_pointerxy()  # Get mouse position
        if self.scrollable_frame.winfo_rootx() <= x <= self.scrollable_frame.winfo_rootx() + self.scrollable_frame.winfo_width() and \
                self.scrollable_frame.winfo_rooty() <= y <= self.scrollable_frame.winfo_rooty() + self.scrollable_frame.winfo_height():
            if self.scrollbar_visible:
                self.canvas.yview_scroll(int(-1 * (event.delta // 120)), "units")

    def on_resize(self, event=None):
        self.after(1, self.adjust_canvas_width)

    def adjust_canvas_width(self):
        self.update_idletasks()
        if self.scrollbar_visible:
            scrollbar_width = self.scrollbar.winfo_width()
            canvas_width = self.winfo_width() - scrollbar_width
        else:
            canvas_width = self.winfo_width()
        self.canvas.itemconfig(self.window_id, width=canvas_width)

    def update_scroll_region(self):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.update_scrollbar_visibility()

    def update_scrollbar_visibility(self):
        content_height = self.canvas.bbox("all")[3]
        canvas_height = self.canvas.winfo_height()
        if content_height > canvas_height:
            if not self.scrollbar_visible:
                self.set_scrollbar_visible(True)
        else:
            if self.scrollbar_visible:
                self.set_scrollbar_visible(False)

    def set_scrollbar_visible(self, state):
        if state:
            self.scrollbar.pack(side="right", fill="y")
            self.scrollbar_visible = True
            self.adjust_canvas_width()
        else:
            self.scrollbar.pack_forget()
            self.scrollbar_visible = False
            self.adjust_canvas_width()

    def destroy(self):
        self.container.unbind("<MouseWheel>")
        super().destroy()

    def clean(self):
        # for recalculate canvas
        placeholder = ttk.Frame(self.scrollable_frame, height=0)
        placeholder.pack()
        self.canvas.update_idletasks()
        self.update_scroll_region()
        placeholder.pack_forget()
        self.update_scroll_region()

    def update_ui(self):
        self.canvas.update_idletasks()
        self.update_idletasks()
        self.update()


if __name__ == "__main__":
    root = tk.Tk()
    frame = ScrollableFrame(root)
    for i in range(15):
        ttk.Label(frame.scrollable_frame, text=f"Sample scrolling label {i + 1}").pack()
        entry_box = tk.Entry(frame.scrollable_frame)
        entry_box.pack(fill=tk.X, expand=True, padx=10, pady=10)
    frame.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
