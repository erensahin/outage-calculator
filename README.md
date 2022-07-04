# outage-calculator

This application is developed and tested in Python 3.8.

## Setting Up

### Setting up the virtual environment

It is suggested to set up a virtual environment to isolate this application from your current environment.

For POSIX systems;

```

python -m venv /path/to/virtual_env
source /path/to/virtual_env/bin/activate

```

For Windows;

```

python -m venv \path\to\virtual_env
\path\to\virtual_env\Scripts\activate.bat

```

See [venv documentation](https://docs.python.org/3/library/venv.html) for more details.

### Install the requirements

After you create your virtual environment and make sure that you are in your virtual environment, you can install requirements.

For running only the application, installing `requirements.txt` should be enough:

```
pip install -r requirements.txt
```

If you are going to do development (i.e. run unit tests), you should install `dev-requirements.txt` as well.

```
pip install -r dev-requirements.txt
```

### Set up the credential file

There is an example credential file located at `assets/credentials.json.example`.
You should put your own credential file in the expected format and expected name, which is `assets/credentials.json`:

```json
{
    "api_key": "",
    "api_url": ""
}
```

To do this, you can copy `assets/credentials.json.example` and rename it as `assets/credentials.json`
And then, you should enter `api_key` and `api_url`

## Running the application

You can run the application from the terminal/command propmt as:

```
python main.py
```

You can also specify different arguments for `site-id` and `start-date`.
But the application will still work if you don't specify these arguments.
For example:

```
python main.py --site-id foo --start-date bar
```

## Running the unit tests

You can run the unit tests with `pytest` package:

```
pytest tests
```

For coverage report, you should use `coverage` package:

```
coverage run --source src -m pytest tests
coverage report
```