from widget.progress_bar import ProgressBar


class ProgressManager:
    def __init__(self, parent):
        self.parent = parent
        self.progress_bar = None

    def create_widgets(self, frame):
        self.progress_bar = ProgressBar(frame, self.parent)
