# Calculate/Saver/WellLogSaver.py
import lasio
import numpy as np
import logging

logger = logging.getLogger(__name__)

class WellLogSaver:
    @staticmethod
    def save_las_file(filepath, well_data):
        try:
            # Собираем данные
            data_dict = {}
            for name in well_data.curve_names:
                curve = well_data.get_curve(name)
                if curve is not None:
                    # Заменяем NaN на -999.25
                    curve_clean = curve.copy()
                    curve_clean[np.isnan(curve_clean)] = -999.25
                    data_dict[name] = curve_clean
            
            if not data_dict:
                return False
            
            # Просто создаем файл через lasio без сложных параметров
            las = lasio.LASFile()
            
            # Только обязательное поле
            las.well['NULL'] = lasio.HeaderItem('NULL', value=-999.25)
            
            # Просто добавляем все кривые как есть
            for name, curve in data_dict.items():
                # Пробуем самый простой способ
                try:
                    # Для старых версий lasio
                    las.add_curve(name, curve)
                except:
                    try:
                        # Для новых версий
                        las.append_curve(name, curve)
                    except:
                        # Просто записываем в data
                        if not hasattr(las, 'data'):
                            las.data = {}
                        las.data[name] = curve
            
            # Сохраняем
            las.write(filepath)
            logger.info(f"Файл сохранен: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка сохранения: {e}")
            return False