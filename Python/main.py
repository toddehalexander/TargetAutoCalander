## main.py
import sys
from PyQt5.QtWidgets import QApplication
from src.gui_app import ScheduleParserGUI

def main():
    app = QApplication(sys.argv)
    ex = ScheduleParserGUI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()