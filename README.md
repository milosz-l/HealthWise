# Installation

## Requirements

- Poetry
- filled `.env` file (copy `.env.example`, rename it, and fill in the missing API keys)

## Install dependencies

```bash
poetry install
```

In case you get this error:
```
... pip install tavily-python
```
then run:
```bash
pip install --upgrade tavily-python
```

## Run the app

```bash
poetry shell
python code/src/server.py
```

## Run pre-commit hooks

For now it's only black formatter.

```bash
pre-commit run --all-files
```

#### TODO
pip install --upgrade tavily-python