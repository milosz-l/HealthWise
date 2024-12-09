# Installation

## Requirements

- Poetry
- Filled `.env` file (copy `.env.example`, rename it, and fill in the missing API keys)

## Install dependencies

```bash
poetry install
```

If you encounter the error `ImportError: cannot import name 'TavilyClient' from 'tavily'`, run the following command:
```
pip install tavily-python
```
then run:
```bash
pip install --upgrade tavily-python
```

## Run the app

### Start the backend server
```bash
poetry shell
python backend/server.py
```

### Start the frontend app
```bash
streamlit run HealthWise.py
```

## Run pre-commit hooks

For now it's only black formatter.

```bash
pre-commit run --all-files
```

#### TODO
pip install --upgrade tavily-python