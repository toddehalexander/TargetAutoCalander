import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel, QFileDialog
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt
from src.schedule_parser import parse_schedule, create_ics_file

class ScheduleParserGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                color: #333333;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
                margin-bottom: 5px;
            }
            QTextEdit {
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 13px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(15)

        self.label = QLabel('Paste your schedule text below (via <a href="https://mytime.target.com/schedule">https://mytime.target.com/schedule</a>):')
        self.label.setOpenExternalLinks(True)
        layout.addWidget(self.label)

        self.textEdit = QTextEdit()
        self.textEdit.setMinimumHeight(200)
        layout.addWidget(self.textEdit)

        self.parseButton = QPushButton('Parse Schedule and Create ICS')
        self.parseButton.clicked.connect(self.parse_and_create_ics)
        layout.addWidget(self.parseButton)

        self.resultLabel = QLabel('')
        self.resultLabel.setWordWrap(True)
        self.resultLabel.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.resultLabel.setOpenExternalLinks(True)
        layout.addWidget(self.resultLabel)

        # Create a container for the links
        self.linkContainer = QWidget()
        linkLayout = QVBoxLayout(self.linkContainer)
        linkLayout.setSpacing(5)

        self.gcalLink = QLabel('<a href="https://calendar.google.com/calendar">Open Google Calendar Landing Page</a>')
        self.gcalLink.setOpenExternalLinks(True)
        self.gcalLink.setAlignment(Qt.AlignCenter)
        linkLayout.addWidget(self.gcalLink)

        self.importLink = QLabel('<a href="https://calendar.google.com/calendar/r/settings/export">Go to Import (Google Calendar)</a>')
        self.importLink.setOpenExternalLinks(True)
        self.importLink.setAlignment(Qt.AlignCenter)
        linkLayout.addWidget(self.importLink)

        self.linkContainer.setStyleSheet("""
            QLabel {
                font-size: 14px;
                margin-top: 5px;
            }
        """)
        self.linkContainer.hide()  # Initially hidden
        layout.addWidget(self.linkContainer)

        self.setLayout(layout)
        self.setGeometry(300, 300, 600, 675)  # Increased height to accommodate the new links
        self.setWindowTitle('Work Schedule Parser')
        self.show()

    def parse_and_create_ics(self):
        schedule_text = self.textEdit.toPlainText()
        parsed_shifts = parse_schedule(schedule_text)

        if not parsed_shifts:
            self.resultLabel.setText("No shifts found. Please check your input.")
            self.linkContainer.hide()
            return

        result_text = "<b>Parsed shifts:</b><br>"
        for shift in parsed_shifts:
            duration_hours = shift['duration'].total_seconds() / 3600
            result_text += f"<p><b>Date:</b> {shift['date'].date()}, <b>Start:</b> {shift['start_time'].strftime('%H:%M')}, " \
                           f"<b>End:</b> {shift['end_time'].strftime('%H:%M')}, " \
                           f"<b>Role:</b> {shift['role']}, <b>Duration:</b> ({duration_hours:.2f} hrs)</p>"

        self.resultLabel.setText(result_text)

        # Create ICS file
        output_dir = QFileDialog.getExistingDirectory(self, "Select Output Directory for ICS File")
        if output_dir:
            ics_result = create_ics_file(parsed_shifts, output_dir)
            self.resultLabel.setText(self.resultLabel.text() + f"<p><b>{ics_result}</b></p>")
            self.linkContainer.show()  # Show the Google Calendar links after successful ICS creation

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ScheduleParserGUI()
    sys.exit(app.exec_())