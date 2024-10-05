import tkinter as tk

from PIL import Image, ImageTk

from util.image_util import resize_image


class IconCheckbox(tk.Label):
    def __init__(self, master, width=15, height=15, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.width = width
        self.height = height
        self.icon_checked = None
        self.icon_checked = None
        self.icon_unchecked = None
        self.is_checked = True
        self.is_enabled = True
        self.resize_img()
        self.set_state(self.is_checked)
        self.bind("<Button-1>", self.toggle)

    def toggle(self, env):
        if self.is_enabled:
            self.is_checked = not self.is_checked
            self.config(image=self.icon_checked if self.is_checked else self.icon_unchecked)
            self.event_generate('<<CheckboxToggled>>', when='tail')

    def set_enabled(self, enabled):
        self.is_enabled = enabled

    def resize_img(self):
        uncheck_image = Image.open('res/icon/checkbox_uncheck.png')
        img = resize_image(uncheck_image, (self.width, self.height))
        self.icon_unchecked = ImageTk.PhotoImage(img)
        checked_image = Image.open('res/icon/checkbox_checked.png')
        img = resize_image(checked_image, (self.width, self.height))
        self.icon_checked = ImageTk.PhotoImage(img)

    def get_state(self):
        return self.is_checked

    def set_state(self, state):
        self.is_checked = state
        self.config(image=self.icon_checked if self.is_checked else self.icon_unchecked, cursor="hand2")

    def pack(self, **kwargs):
        super().pack(**kwargs)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Icon Checkbox Example")
    icon_checked = tk.PhotoImage(file="res/icon/checkbox_checked.png")
    icon_unchecked = tk.PhotoImage(file="res/icon/checkbox_uncheck.png")
    icon_checkbox = IconCheckbox(root)
    icon_checkbox.pack(pady=20)
    icon_checkbox.set_enabled(True)
    root.mainloop()
