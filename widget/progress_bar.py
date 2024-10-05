import threading
import time
import tkinter as tk
from tkinter import ttk

from ttkbootstrap import Style

from util.event_bus import event_bus


class ProgressBar:
    def __init__(self, parent, root):
        self.root = root
        self.parent = parent
        self.style = Style(theme='litera')
        self.style.configure("green.Horizontal.TProgressbar",
                             troughcolor='white',
                             background='green',
                             thickness=30)
        self.frame = tk.Frame(parent, bg="white")
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=0)
        self.progress = ttk.Progressbar(self.frame, style="green.Horizontal.TProgressbar",
                                        orient="horizontal", length=300, mode="determinate")
        self.progress.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.progress["maximum"] = 100
        self.progress["value"] = 0
        self.frame.columnconfigure(0, weight=1)
        self.progress_text = tk.Label(self.frame, text="", font=("Arial", 12, "bold"), bg="white")
        self.progress_text.pack(side=tk.LEFT, fill=tk.X, padx=0)
        event_bus.subscribe("UpdateProgress", self.update_progress)
        self.total_count = 100
        self.current_finish_count = 0
        self.last_update_time = 0
        self.root.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        self.update_progress_text(self.progress["value"])

    def start_thread(self):
        threading.Thread(target=self.run_task, daemon=True).start()

    def run_task(self):
        for i in range(180):
            time.sleep(0.005)
            self.go_forward(1)

    def set_total_count(self, count):
        self.total_count = count

    def clean(self):
        self.current_finish_count = 0
        self.update_progress(0)
        self.progress_text.config(text="")

    def go_forward(self, count):
        if self.total_count == 0:
            return
        current_time = time.time()
        self.current_finish_count += count
        if (current_time - self.last_update_time) >= 0.01 or self.current_finish_count + count >= self.total_count:
            self.last_update_time = current_time
            value = 100 * float(self.current_finish_count) / self.total_count
            event_bus.publish("UpdateProgress", value=value)

    def update_progress(self, value):
        if value >= 100:
            value = 100
        self.root.after(0, self.progress.configure, {"value": value})
        self.update_progress_text(value)


    def update_progress_text(self, value):
        if value == 0:
            return
        current_finish_count = f"{self.current_finish_count} | {self.total_count}"
        self.progress_text.config(text=current_finish_count)
        self.frame.update_idletasks()
        self.progress_text.update()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("progress")
    root.geometry("500x100")
    root.minsize(300, 100)
    app = ProgressBar(root, root)
    app.set_total_count(200)
    app.start_thread()
    root.mainloop()
