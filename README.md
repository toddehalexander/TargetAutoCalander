# Work Schedule Parser

This application helps Target employees parse their work schedules and create ICS files for easy import into calendar applications.

### Web-Based Version
https://toddehalexander.github.io/TargetAutoCalander/ 

In addition to the Python-based desktop application, this tool is now also available as a web application. You can use it directly in your browser without any installation. Just visit the web page, paste your schedule, and download the ICS file.

## Web Usage GIF
![Web Usage GIF](https://github.com/toddehalexander/TargetAutoCalander/blob/main/assets/web_usage.gif)

## Python Usage GIF
![Python Usage GIF](https://github.com/toddehalexander/TargetAutoCalander/blob/main/assets/python_usage.gif)


## [Example ICS file output (click to view file)](https://github.com/toddehalexander/TargetAutoCalander/blob/main/sample_output/work_schedule_Jun09-Jun15_2024.ics "Example Output")
![ICS File](https://github.com/toddehalexander/TargetAutoCalander/blob/main/assets/ICS_Example.png) 


## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone this repository or download the source code.

2. Navigate to the project directory in your terminal or command prompt.

3. Install the required dependencies by running: ```pip install -r requirements.txt```

This will install the necessary Python packages, including PyQt5.

## Usage

1. Open a terminal or command prompt.

2. Navigate to the directory containing the script.

3. Run the application by executing: ```python main.py```

4. The application window will open.

5. Copy your work schedule from the Target MyTime website (https://mytime.target.com/schedule).
   - CNTRL + A to select all, CNTRL + C to copy, CNTRL + V to paste into the box

7. Paste the copied schedule text into the text area in the application.

8. Click the "Parse Schedule and Create ICS" button.

9. Choose a directory to save the ICS file when prompted.

10. The application will display the parsed shifts and create an ICS file in the selected directory.

11. After successful creation, two links will appear at the bottom of the window:
 - "Open Google Calendar": Opens the main Google Calendar page.
 - "Go to Import/Export": Takes you directly to the Import/Export settings in Google Calendar.

11. Use these links to quickly navigate to Google Calendar and import your newly created ICS file.

## Troubleshooting

- If you encounter any issues with parsing, make sure you've copied the entire schedule text correctly from the Target MyTime website.
- Ensure that you have the necessary permissions to write files in the directory you choose for saving the ICS file.

## Support

If you encounter any problems or have any questions, please open an issue in this repository.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
