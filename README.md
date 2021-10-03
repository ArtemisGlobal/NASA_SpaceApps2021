# NASA_SpaceApps2021
Nasa Space Apps Challenge 2021

This will provide a backend API for the spaceapps challenge based on Flask.

## Installation

MySQL needs to be installed and started.
I followed [this guide](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04) to get mysql installed and running on Ubuntu (Linux).

Once MySQL is installed, we need to install python 3.8.5.
Install [Python 3.8.10](https://www.python.org/downloads/release/python-3810/)

After Python is installed, install the Python packages using:

```shell
python3 -m venv hackathon 
source hackathon/bin/activate
pip install -r requirements.txt
```

## Running

After things have been installed, the server can be started.
We will need to export the name of the file to run.

```shell
EXPORT FLASK_APP=api
flask run --host=0.0.0.0
```

## API

You must be logged in to interact with the API.
To log in go to the `/login` endpoint.
If you are logged in as a public profile, you may only retrieve data.
If you are logged in as not public, you can upload things to the database as well as retrieve.
