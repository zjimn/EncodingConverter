import Pmw


class Tooltip:
    def __init__(self, parent):
        self.parent = parent
        self.tooltip = Pmw.Balloon(self.parent)

    def bind(self, data):
        widget, text = data
        self.tooltip.bind(widget, text)

    def unbind(self, data):
        for widget in data:
            self.tooltip.unbind(widget)
