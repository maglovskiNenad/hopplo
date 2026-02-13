# TIPPLY 

Automatically read and clean exported CSV files with employees’ working hours. 
The app detects and handles different file encodings using the Chardet library, 
supports a drag-and-drop interface for intuitive file uploads, and extracts only 
confirmed work hours (‘Bestätigte Arbeitszeit’) for accurate calculations. It also loads daily 
tip amounts from a separate tab-separated file, matches each employee’s working hours 
with the relevant day’s tip amount, calculates fair tip distribution proportionally based on hours worked, and presents the final results in a clean, formatted table inside the app.