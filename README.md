# MOOdle

![Workflow status](https://github.com/NovAti0n/Statify/actions/workflows/main.yml/badge.svg)

Website for LINFO1002-P2

[Commit guidelines](https://github.com/obsproject/obs-studio/blob/master/CONTRIBUTING.rst#commit-guidelines)

## Initial setup

**Before proceeding, make sure that you at least have Python 3.10 installed as `python3`. On some Linux distros, you may have to substitute `python3` for `python3.10`. On Windows, `python3` must be substituted by `python` or `py`.**

Create a Python virtual environment and activate it.

On Linux:

```sh
% python3 -m venv env
% source env/bin/activate
```

On Windows:

```powershell
% python -m venv env
% .\env\Scripts\activate
```

Install the requirements with `pip`:

```sh
(env) % pip install -r requirements.txt
```

(If this command isn't recognized, use `python3 -m pip install -r requirements.txt` instead).

You can deactivate the virtual environment by issuing:

```sh
(env) % deactivate
```

## Running Flask app

Make sure your virtual environment is still activated.

On Linux:

```sh
% source env/bin/activate
```

On Windows:

```powershell
% python -m venv env
% .\env\Scripts\activate
```

Generate the database:

```sh
% flask init-db
```

This process can take up to 2 minutes. Be patient.

Start the server:

```sh
% flask run
```

### Running in development environment

If you need Flask to run in development mode (enables live reload among other things), define an environment variable called `FLASK_ENV` with the value `development`.

On Linux:

```sh
% export FLASK_ENV="development"
```

On Windows (PowerShell):

```powershell
% $env:FLASK_ENV="development"
```

## `pre-commit` hook

The pre-commit hook does various things such as:

-   Making sure there are no terminated whitespaces in staged files
-   Making sure commit message does not contain non-ASCII characters
-   Making sure that the code complies with the `.editorconfig` rules

### Enabling

To enable the hook (highly recommended), copy the `.git-templates/hooks/pre-commit` file to `.git/hooks/pre-commit`:

```sh
% cp .git-templates/hooks/pre-commit .git/hooks/pre-commit
```

### Bypassing

If you need to bypass this hook, use the `--no-verify` option:

```sh
% git commit -m "db: Detailed commit message" --no-verify
```

## Directory structure road guide

|Path|Description|
|-|-|
|`.github/workflows`|GitHub CI/CD workflows.|
|`public/static`|Resources used by the webapp. This includes CSS stylesheets, GLSL vertex & fragment shaders, Javascript code (notably for chart rendering) and, finally, textures, images, models, and other graphics.|
|`public/templates`|HTML code for all the different route templates.|
|`src`|Server code.|
|`work`|Working files, e.g. Blender projects for 3D models.|
