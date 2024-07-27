# Simple chatbot reservation agent

A simple chatbot capable of taking reservation user inputs and saving them into csv file.
How-to:
1. Install necessary dependencies, run `pip install -r requirements_pip.txt` for python environment or `conda create --name <env> --file requirements_conda.txt` for a conda environment.
2. Run `python -m spacy download en_core_web_md` to download spacy languange data.
3. Run `rasa train` to train chatbot based on the given data.
4. Run `rasa run --enable-api --cors "*"` for the chatbot agent on one terminal and `rasa run actions` for the chatbot actions server on another terimanl.
5. Run `flask run` for the web app on another terminal.
6. Access localhost:5000 for the web app.
7. Do a reservation!
8. The data will be saved on appointments.csv on the project folder.

Made with rasa
