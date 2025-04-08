# Form Manager - backend

A system  for handling form submissions.

## Install dependencies

The following command ensures that all project dependencies are installed and up-to-date with the lockfile.
It also creates a virtual environment in `.venv` if it doesn't exist yet.

```bash
uv sync
```

## Upgrade dependencies

With an existing `uv.lock` file, `uv` will always prefer the previously locked versions of packages.

To upgrade all locked package versions:

```bash
uv lock --upgrade
```

To upgrade a specific locked package version:

```bash
uv lock --upgrade-package <package>
```

To synchronise the environment with the lockfile:

```bash
uv sync
```

Alternatively, if you feel confident, all in one:

```bash
uv sync --upgrade
```

## Start the app in development mode (hot-code reloading, error reporting, etc.)

```bash
flask run --host 0.0.0.0 --port 5000
```

## Lint the files

```bash
ruff check
```

## Format the files

```bash
ruff format
```

## Run the tests

You need an accessible MongoDB instance to run the tests:

``` bash
pytest --color=yes --cov=./ --cov-report=xml:./tests/coverage/report.xml tests/
```
