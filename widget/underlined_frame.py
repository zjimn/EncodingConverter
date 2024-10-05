import tkinter as tk


class UnderlinedFrame:
    def __init__(self, root, frame_width=250, frame_height=1, line_color="#A9A9A9", padx=0, pady=0):
        self.root = root
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.line_color = line_color
        self.frame = tk.Frame(self.root, bg="gray", width=self.frame_width, height=self.frame_height)
        self.frame.pack(side=tk.TOP, padx=padx, pady=pady, fill=tk.X, expand=False)
        self.canvas = tk.Canvas(self.frame, height=2, bg="#E0E0E0", highlightthickness=0)
        self.canvas.pack(fill=tk.X)
        self.line = self.canvas.create_line(0, 1, self.frame_width, 1, fill=self.line_color)
        self.canvas.bind("<Configure>", self.adjust_canvas_width)

    def adjust_canvas_width(self, event):
        canvas_width = event.width
        self.canvas.coords(self.line, 0, 1, canvas_width, 1)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x200")
    underlined_frame = UnderlinedFrame(root)
    root.mainloop()
