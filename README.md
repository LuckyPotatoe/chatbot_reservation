# Simple chatbot reservation agent

A simple chatbot capable of taking reservation user inputs and saving them into csv file.
How-to:
1. Install necessary dependencies, run `pip install -r requirements.txt` for python environment or `conda create --name <env> --file requirements_conda.txt` for a conda environment.
2. Run `rasa run --enable-api --cors "*"` for the chatbot agent on one terminal and `rasa run actions` for the chatbot actions server on another terimanl.
3. Run `flask run` for the web app on another terminal.
4. Access localhost:5000 for the web app.
5. Do a reservation!
6. The data will be saved on appointments.csv on the project folder.

Made with rasa
