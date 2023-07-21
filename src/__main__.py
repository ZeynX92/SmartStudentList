import sys
from forms.main_window import SmartStudentList
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SmartStudentList()
    ex.show()
    sys.exit(app.exec())
