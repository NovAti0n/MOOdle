# Statify
Website for LINFO1002-P2

[Commit guidelines](https://github.com/obsproject/obs-studio/blob/master/CONTRIBUTING.rst#commit-guidelines)

## Initial setup

**Make sure, before proceeding, that you at least have Python 3.10 installed as `python3`**
Create a Python virtual environment and activate it:

```sh
% python3 -m venv env/
% source env/bin/activate
```

Install the requirements with `pip`:

```sh
(env) % python3 -m pip install -r requirements.txt
```

(It's important to use the `python3 -m` prefix; not sure why nor do I care why.)
You can deactivate the virtual environment by issuing:

```sh
(env) % deactivate
```

## Running flask app

Make sure your virtual environment is still activated:

```sh
% source env/bin/activate
```

Then, set the relevant Flask environment variables and run:

```sh
% export FLASK_ENV=development # nothing to do with virtual environments
% export FLASK_APP=main # entrypoint for the app
% flask run
```
