# Installation

## Requirements

- Poetry
- filled `.env` file (copy `.env.example`, rename it, and fill in the missing API keys)

## Install dependencies

```bash
poetry install
```

## Optional: Setpu KG-RAG

### Step 1: Install dependencies

```
pip install -r requirements.txt
```

### Step 2: Update config.yaml 

**config.yaml** holds all the necessary information required to run the scripts on your machine. Make sure to populate it accordingly.

### Step 3: Run the setup script
Note: Make sure you are in KG_RAG folder

Setup script runs in an interactive fashion.

Running the setup script will: 

- create disease vector database for KG-RAG
- download Llama model in your machine (optional, you can skip this and that is totally fine)

```
python -m kg_rag.run_setup
```

## Run the app

```bash
poetry shell
python code/src/server.py
```
