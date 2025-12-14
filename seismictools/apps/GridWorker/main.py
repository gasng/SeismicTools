import sys
from PyQt5.QtWidgets import QApplication
from UI.View.ViewWidget import ViewWidget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ViewWidget()
    window.show()
    sys.exit(app.exec_())
