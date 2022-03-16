# Statify
Website for LINFO1002-P2

[Commit guidelines](https://github.com/obsproject/obs-studio/blob/master/CONTRIBUTING.rst#commit-guidelines)

## Initial setup

**Make sure, before proceeding, that you at least have Python 3.10 installed as `python3`. If you're on a retarded Linux distro, you may have to substitute `python3` for `python3.10`**

Create a Python virtual environment and activate it:

```sh
% python3 -m venv env
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

## Running Flask app

Make sure your virtual environment is still activated:

```sh
% source env/bin/activate
```

Start the server:

```sh
% flask run
```

If you need Flask to run in development mode (enables live reload among other things), rename the file `.flaskenv.example` to `.flaskenv` and uncomment the line starting with `FLASK_ENV` in this file. You can then start the server with the same command as above.

## `pre-commit` hook

The pre-commit hook does various things such as:

- Making sure there are no terminated whitespaces in staged files
- Automatically unstaging `.flaskenv` (the version on remote is meant as an *example*)
- Probably some other stuff in `.git/hooks/pre-commit.sample` idk

If you need to bypass this hook, such as when modifying the contents of the example `.flaskenv` file, use the `--no-verify` option:

```sh
% git commit -S -m "flaskenv: Detailed commit message" --no-verify
```
