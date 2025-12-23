# Calculate/Data/WellLogData.py
import logging
import numpy as np

logger = logging.getLogger(__name__)

class WellLogData:
    def __init__(self):
        self.filename = ""
        self.curves = {}
        self.curve_names = []
        self.class_labels = None
        self.class_names = {}
        self.class_colors = {}
        self.metadata = {}

    def get_class_color(self, class_id):
        return self.class_colors.get(class_id, "#808080")

    def set_filename(self, filename):
        self.filename = filename

    def add_curve(self, name, data):
        self.curves[name] = np.array(data)
        if name not in self.curve_names:
            self.curve_names.append(name)

    def get_curve(self, name):
        return self.curves.get(name, None)

    def get_curve_names(self):
        return self.curve_names.copy()

    def set_class_labels(self, labels):
        self.class_labels = np.array(labels)

    def get_class_labels(self):
        return self.class_labels

    def add_class(self, class_id, class_name, color):
        self.class_names[class_id] = class_name
        self.class_colors[class_id] = color

    def get_class_name(self, class_id):
        return self.class_names.get(class_id, f"Класс {class_id}")

    def get_class_color(self, class_id):
        return self.class_colors.get(class_id, "#808080")

    def get_num_points(self):
        if len(self.curve_names) > 0:
            return len(self.curves[self.curve_names[0]])
        return 0

    def clear(self):
        self.filename = ""
        self.curves.clear()
        self.curve_names.clear()
        self.class_labels = None
        self.class_names.clear()
        self.class_colors.clear()
        self.metadata.clear()

    def remove_curve(self, curve_name):
        if curve_name in self.curves:
            del self.curves[curve_name]
            self.curve_names.remove(curve_name)
            logger.debug(f"Кривая удалена: {curve_name}")
            return True
        return False