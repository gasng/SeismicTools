import numpy as np

class WellLogData:
    def __init__(self, well_name):
        self.well_name = well_name
        self.depth_las = 'DEPT'
        self.meta = {}
        self.curves = {}
        self.length = 0

    def set_curves(self, curves, depth_las):
        """Установить кривые для скважины"""
        if not curves:
            raise ValueError('Нет кривых')
        
        lengths = {len(array) for array in curves.values()}
        if len(lengths) != 1:
            raise ValueError('Кривые разной длины')
        
        self.length = lengths.pop()
        self.curves = curves
        self.depth_las = depth_las
        
        if depth_las not in self.curves:
            raise KeyError(f"Кривая глубины '{depth_las}' не найдена")

    def depth(self):
        """Получить массив глубин"""
        return self.curves.get(self.depth_las, np.array([]))

    def curve_names(self):
        """Получить список имен кривых"""
        return list(self.curves.keys())

    def add_curve(self, name, data):
        """Добавить новую кривую"""
        if len(data) != self.length:
            raise ValueError(f'Длина кривой {name} ({len(data)}) не совпадает с длиной данных ({self.length})')
        self.curves[name] = data

    def assign_class_labels(self, indices: list, class_label: int):
        """Присвоить метку класса указанным индексам глубин"""
        if "CLASS" not in self.curves:
            self.curves["CLASS"] = np.full(self.length, -1, dtype=int)
        self.curves["CLASS"][indices] = class_label

    def get_points_for_crossplot(self, x_name, y_name):
        x = self.curves[x_name]
        y = self.curves[y_name]
        d = self.curves[self.depth_las]
        
        valid = (np.isnan(x) == False) & (np.isnan(y) == False)
        
        return x[valid], y[valid], d[valid], np.arange(self.length)[valid]