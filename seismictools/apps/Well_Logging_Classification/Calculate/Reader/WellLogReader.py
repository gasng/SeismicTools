import lasio
import numpy as np
from ..Data.WellLogData import WellLogData

class WellLogReader:
    """Читает LAS-файл и возвращает объект WellLogData"""

    def read_las(self, file_path):
        """
        Читает LAS-файл по пути.
        
        Args:
            file_path: путь к .las файлу
            
        Returns:
            WellLogData: объект с данными скважины
            
        Raises:
            ValueError: если файл повреждён или пуст
            IOError: если файл не найден
        """
        try:
            las = lasio.read(file_path)

        except Exception as e:
            raise ValueError(f"Не удалось открыть файл '{file_path}': {e}")

        if not las.curves:
            raise ValueError("LAS-файл не содержит кривых")

        curves = {}
        for curve in las.curves:
            data = curve.data
            if hasattr(data, 'filled'):
                data = data.filled(np.nan)
            curves[curve.mnemonic] = np.asarray(data, dtype=np.float64)

        depth_candidates = ["DEPT", "DEPTH"]
        depth_las = None

        for name in depth_candidates:
            if name in curves:
                depth_las = name
                break

        if depth_las is None:
            for name in curves.keys():
                if "DEPT" in name.upper() or "DEPTH" in name.upper():
                    depth_las = name
                    break

        if depth_las is None:
            raise ValueError("Не найдена кривая глубины DEPT или DEPTH")

        well_name = "Unknown"
        if hasattr(las.well, 'WELL') and las.well.WELL.value:
            well_name = las.well.WELL.value

        well_data = WellLogData(well_name=well_name)

        well_data.meta = {}
        for item in las.well:
            well_data.meta[item.mnemonic] = {
                'value': item.value,
                'unit': item.unit,
                'descr': item.descr
            }

        well_data.set_curves(curves, depth_las=depth_las)

        return well_data