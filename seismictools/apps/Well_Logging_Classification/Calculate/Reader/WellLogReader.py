# Calculate/Reader/WellLogReader.py

import lasio
import numpy as np

class WellLogReader:
    @staticmethod
    def read_las_file(filepath):
        try:
            las = lasio.read(filepath)
            curves = {}
            
            for curve in las.curves:
                # Конвертируем прямо в float, заменяя None на NaN
                data = np.array(curve.data, dtype=float)
                data[data == -999.25] = np.nan  # Стандартное значение NULL
                curves[curve.mnemonic] = data
            
            # Убедимся, что есть DEPT
            if 'DEPT' not in curves:
                if curves:
                    first_key = list(curves.keys())[0]
                    num_points = len(curves[first_key])
                    curves['DEPT'] = np.arange(num_points)
            
            return {
                'curves': curves,
                'metadata': {},
                'filename': filepath
            }
        except Exception as e:
            raise ValueError(f"Ошибка при чтении LAS-файла: {str(e)}")