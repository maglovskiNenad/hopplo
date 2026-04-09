# TIPPLY 

Automatically read and clean exported CSV files with employees’ working hours. 
The app detects and handles different file encodings using the Chardet library, 
supports a drag-and-drop interface for intuitive file uploads, and extracts only 
confirmed work hours (‘Bestätigte Arbeitszeit’) for accurate calculations. It also loads daily 
tip amounts from a separate tab-separated file, matches each employee’s working hours 
with the relevant day’s tip amount, calculates fair tip distribution proportionally based on hours worked, and presents the final results in a clean, 
formatted table inside the app.

# Project Description

This Python application automatically reads and processes exported CSV files containing employees’ working hours to fairly distribute tips based on actual hours worked.

Key features include:

•	Detects and handles different file encodings using the Chardet library.

•	Intuitive drag-and-drop interface for file uploads.

•	Extracts only confirmed work hours (‘Bestätigte Arbeitszeit’) for accurate calculations.

•	Loads daily tip amounts from a separate tab-separated file.

•	Matches each employee’s working hours with the corresponding daily tip amount.

•	Calculates fair tip distribution proportionally based on hours worked.

•	Presents the final results in a clean, formatted table within the app.

This project enables quick and precise tip calculations for teams, eliminating manual errors and saving time.

Installation

1. Prerequisites
	•	Python ≥ 3.10
	•	pip (Python package manager)

2. Clone the repository

	     git clone https://github.com/username/tipply_app.git
	     cd hopplo

3. Create a virtual environment (recommended)
									
		python -m venv venv
		source venv/bin/activate   # Linux/macOS
		venv\Scripts\activate      # Windows

4. Install dependencies

		pip install -r requirements.txt

## Release build

Prebuilt desktop packages can be attached to GitHub Releases.

Local release build:

```bash
pip install -r requirements-build.txt
pyinstaller --clean hopplo.spec
```

The packaged app will be created in `dist/hopplo/`.

Automated GitHub Release build:

1. Push a tag like `v1.0.1`
2. GitHub Actions workflow `Build Release` builds packages for Linux, Windows, and macOS
3. The generated archives are uploaded to the matching GitHub Release automatically

## Usage

1.	Run the application:
							
		python main.py

2.	Upload the CSV file containing employees’ working hours using drag-and-drop or file browsing.
3.	Upload the tab-separated file with daily tip amounts.
4.	The app will automatically:

	•	Clean and format the data

	•	Match working hours with daily tips

	•	Calculate proportional tip distribution

5.	Results are displayed in a clear table, ready to export or print.
 
## Project Structure

	tipply_app/
	│
	├─ app/                     # Main application package
	│   ├─ images/              # Image assets used in the app
	│   ├─ config.py            # Configuration settings
	│   ├─ home_page.py         # Home page UI logic
	│   ├─ main.py              # Entry point of the application
	│   ├─ popup.py             # Popup dialogs and messages
	│   ├─ settings.py          # Settings page logic
	│   ├─ tests.py             # Unit tests for the app
	│   ├─ trinkgeld_actions.py # Tip calculation and data processing logic
	│   ├─ update.py            # Update checking logic
	│   ├─ version.txt          # Current app version
	│   └─ warning_msg.py       # Warning and error messages
	│
	├─ .gitignore               # Git ignore rules
	├─ LICENSE                  # MIT License file
	├─ README.md                # Project documentation
	└─ requirements.txt         # Python dependencies


## License

This project is licensed under the MIT License – feel free to use, modify, and distribute.

## Contributing

We welcome contributions! To contribute:
1.	Fork the repository
2.	Create a new branch for your feature:

		git checkout -b feature/new-feature

3.	Make your changes and test thoroughly
4.	Submit a Pull Request with a clear description

Contribution guidelines:

•	Use black or flake8 for code formatting

•	Add tests for new functionality

•	Write clear, readable code with comments where necessary
