import lasio
import numpy as np

class WellLogSaver:
    """Сохраняет WellLogData в LAS-файл."""

    def save_las(self, well_data, file_path: str):
        """
        Сохраняет данные скважины в LAS-файл.

        Args:
            well_data: объект WellLogData
            file_path: путь для сохранения .las файла
        """
        las = lasio.LASFile()

        null_value = -999.25

        well_keys = ['WELL', 'UWI', 'STRT', 'STOP', 'STEP', 'NULL', 'COMP', 'SRVC', 'DATE', 'PROV', 'FLD', 'LOC']
        for key in well_keys:
            if key in well_data.meta:
                item = well_data.meta[key]
                las.well.append(lasio.HeaderItem(
                    mnemonic=key,
                    unit=item.get('unit', ''),
                    value=item.get('value', ''),
                    descr=item.get('descr', '')
                ))
                if key == 'NULL':
                    null_value = item['value']

        for curve_name, data_array in well_data.curves.items():

            clean_data = np.where(np.isnan(data_array), null_value, data_array)
            las.append_curve(
                mnemonic=curve_name,
                data=clean_data,
                unit='',
                descr=''
            )

        las.write(file_path, version=2.0)