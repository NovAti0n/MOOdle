# MOOdle

![Workflow status](https://github.com/NovAti0n/MOOdle/actions/workflows/main.yml/badge.svg)

Advanced cow visualization tool.

![Paturage mode](eyecandy/paturage.png)

## Initial setup

**Before proceeding, make sure that you at least have Python 3.10 installed as `python3`. On some Linux distros, you may have to substitute `python3` for `python3.10`. On Windows, `python3` may be substituted by `python` or `py`.**

Create a Python virtual environment and activate it.

On realOS (i.e. most Unix-like OS', such as Linux, FreeBSD, or macOS):

```console
python3 -m venv env
source env/bin/activate
```

On Windows:

```console
python -m venv env
.\env\Scripts\activate
```

Install the requirements with `pip`:

```console
pip install -r requirements.txt
```

(If this command isn't recognized, use `python3 -m pip install -r requirements.txt` instead).

You can deactivate the virtual environment by issuing:

```console
deactivate
```

## Running Flask app

Make sure your virtual environment is still activated.

On realOS:

```console
source env/bin/activate
```

On Windows:

```console
.\env\Scripts\activate
```

Generate the database:

```console
flask init-db
```

This process can take up to 2 minutes. Be patient.

Start the server:

```console
flask run
```

### Running in development environment

If you need Flask to run in development mode (enables live reload among other things), define an environment variable called `FLASK_ENV` with the value `development`.

On realOS:

```console
export FLASK_ENV="development"
```

On Windows (PowerShell):

```console
$env:FLASK_ENV="development"
```

## Directory structure

| Path                | Description                                                                                                                                                                                  |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `.github/workflows` | GitHub CI/CD workflows.                                                                                                                                                                      |
| `public/static`     | Resources used by the webapp. This includes CSS stylesheets, GLSL vertex & fragment shaders, Javascript code (notably for chart rendering) and textures, images, models, and other graphics. |
| `public/templates`  | HTML code for all the different route templates.                                                                                                                                             |
| `src`               | Server code.                                                                                                                                                                                 |
| `work`              | Working files, e.g. Blender projects for 3D models.                                                                                                                                          |

## Contributing

We follow OBS commit guidelines, more info [here](https://github.com/obsproject/obs-studio/blob/master/CONTRIBUTING.rst#commit-guidelines).

Before contributing to MOOdle, you need to install some tools to check that your code follows our code style.

### `editorconfig-checker`

Install `editorconfig-checker` by running the following command in your virtual environment:

```console
pip install editorconfig-checker
```

### `pre-commit` hook

The pre-commit hook does various things such as:

-   Making sure there are no terminated whitespaces in staged files
-   Making sure commit message does not contain non-ASCII characters
-   Making sure that the code complies with the `.editorconfig` rules

#### Enabling

To enable the hook (highly recommended), copy the `.git-templates/hooks/pre-commit` file to `.git/hooks/pre-commit`:

```console
cp .git-templates/hooks/pre-commit .git/hooks/pre-commit
```

#### Bypassing

If you need to bypass this hook, use the `--no-verify` option:
Bypassing is generally a bad idea, since this hook is also run in the GitHub workflow.

```console
git commit -m "db: Detailed commit message" --no-verify
```

## More screenshots

![Also in white](eyecandy/velages.png)
![And with a responsive design (for mobile)](eyecandy/lune.png)

## Authors

- Alexis Englebert ([@alexisloic21](https://github.com/alexisloic21))
- Noa Quenon ([@NovAti0n](https://github.com/NovAti0n))
- Aymeric Wibo ([@obiwac](https://github.com/obiwac))
