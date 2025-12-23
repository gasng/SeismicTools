import sys
import logging
from pathlib import Path
from PySide6.QtWidgets import QApplication
from seismictools.apps.Well_Logging_Classification.UI.MainWindow import MainWindow

def setup_logging():
    log_file = Path(__file__).parent / "well_classifier.log"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

def main():
    logger = setup_logging()
    logger.info("Запуск")

    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        logger.info("Приложение запущено!")
        sys.exit(app.exec())
    except Exception as e:
        logger.exception("ОШИБКА ПРИ ЗАПУСКЕ")
        sys.exit(1)

if __name__ == "__main__":
    main()