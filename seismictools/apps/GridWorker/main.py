import sys
from PyQt5.QtWidgets import QApplication
from seismictools.apps.GridWorker.UI.View.ViewWidget import ViewWidget

def main():
    app = QApplication(sys.argv)
    window = ViewWidget()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

