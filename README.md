# HealthWise

**Multi-agent healthcare system: trusted health assistant for people, outbreak detector for health authorities.**

Main features:
- Multi-agent system (*LangGraph*, *LangChain*)
- Chatbot **responses** are **grounded ONLY on reliable sources**: 
    - nhs.uk
    - medlineplus.gov
    - cdc.gov
- Outbreak detector for health authorities - **analysis panel for health authorities** with visualisations and forecasting

## Demo video
[![HealthWise Demo](docs/figures/play_video_thumbnail.png)](https://youtu.be/ZP9zoNelaC4 "Watch the demo video")
***Click above to watch the demo video!***

## Tech stack
- **Backend**: Python, FastAPI, LangGraph, LangChain
- **Frontend**: Streamlit
- **LLM**: OpenAI (gpt-4o and gpt-4o-mini)
- **Search engine**: Tavily
- **Visualisation**: Plotly
- **Virtual environment**: Matplotlib
- **Data storage**: MongoDB

## Security considerations
- The app is seperated into two parts: chatbot for people and analysis panel for health authorities.
    - Chatbot is public and can be used by anyone. **It can ONLY WRITE to the database, not read from it.**
    - Analysis panel is supposed to be accessed only by health authorities. **It can ONLY READ from the database.**

## Installation

### Requirements

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

## Deployment

Prerequisites:
- **Docker**: Install Docker on your local machine.

### Local deployment

#### Build and run Docker containers

You can start both containers with docker compose with:

```bash
docker-compose up --build
```

### Deployment in the cloud

#### Step 1: Build Docker images

Prerequisites:
- **Terraform**: Install Terraform on your local machine.

#### Step 1: Deploy to the cloud

##### Option 1: AWS
Prerequisites:
- **AWS CLI**: Install and configure AWS CLI on your local machine.
    - enable AWS CLI on your local machine: `aws configure`
        - you can get Access key for your IAM account from the AWS console
        - in AWS console you can also find your AWS account ID, which is needed for the next step
- create two ECR repositories through AWS console: `healthwise-backend` and `healthwise-frontend`
    - both should be mutable
- fill in the `docker-compose.yml.aws.example` file with your AWS account ID and region and rename it to `docker-compose.yml`

Firstly, authenticate Docker with ECR (remember to replace `<your-aws-region>` and `<your-aws-account-id>` with your AWS region and account ID):
```bash
aws ecr get-login-password --region <your-aws-region> | docker login --username AWS --password-stdin <your-aws-account-id>.dkr.ecr.<your-aws-region>.amazonaws.com
```

Secondly, build the Docker images:
```bash
docker-compose up --build
```
NOTE: If you get warnings about environment variables, set them manually in the terminal like this (example for `MONGO_URI`):
```bash
export MONGO_URI=<your-mongo-uri>
```

After successful build, you can turn off the containers.

Thirdly, push the Docker images to ECR:
```bash
docker-compose push
```

Before running Terraform script, go to `EC2 -> Key Pairs -> Create key pair` and download the key pair:
- key pair name: `healthwise-key-name` (needs to match the key pair name in the `terraform/aws/terraform.tfvars` file)
- type: `RSA`
Then, put the downloaded key pair file in the `terraform/aws/` directory.

Now, run the Terraform script:
```bash
cd terraform/aws
terraform init
terraform apply
```

Alternatively (in case of problems that's how you can debug) - create docker-compose.yml file manually and run it:
```bash
nano docker-compose.yml
sudo docker-compose up -d
```
NOTE: The docker compose above is for running the docker images. So it should be based on the docker compose in `terraform/aws/main.tf` file instead of the `docker-compose.yml.aws.example` file which is for building the images locally and pushing them to ECR.

After `terraform apply` is finished, **make sure that the EC2 instance finished initializing in the AWS console** (if the `Status check` is still `initializing`, wait for it to finish - it can take few minutes). Then, you can access the app through browser like this: `http://<ec2-instance-public-ip>:8501`.
