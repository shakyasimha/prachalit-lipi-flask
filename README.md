# Prachalit Lipi Flask Web Application

## What is this web app about?
Simply, it is a last resort for our final year major project, making sure the app runs any way possible

## How to run it?
After cloning the repository,  `cd` into the directory and run `python -m venv venv` to create a virtual environment. 

For Windows users, run `venv/Scripts/Activate.ps1` on the powershell.
For Linux/Mac users, run `source venv/bin/activate` on the terminal.

After activating the virtual environment, run `pip install -r requirements.txt` which installs all the necessary dependencies for the application.
Then run `FLASK_APP=app.py` and `flask run --debug`, the app should be good to go.