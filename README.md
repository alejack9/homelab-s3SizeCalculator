# S3 Size Calculator

Flask server that caches and returns the total usage of an S3 server.

## Usage

### Docker Compose

Create .env file with

| Variable Name           | Value            |
|-------------------------|------------------|
| AWS_ACCESS_KEY_ID       | your-id          |
| AWS_SECRET_ACCESS_KEY   | your-key         |
| AWS_DEFAULT_REGION      | your-region      |
| S3_ENDPOINT_URL         | your-url         |
| S3_GB_PLAN_CAP          | plan-cap-in-gb   |


Run with docker compose

```bash
docker compose up -d --build
```

### Pip

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

```bash
pip install --no-cache-dir -r requirements.txt
```

Set the env variables and run app.py

```bash
AWS_ACCESS_KEY_ID=your-id \
AWS_SECRET_ACCESS_KEY=your-key \
AWS_DEFAULT_REGION=your-region \
S3_ENDPOINT_URL=your-url \
S3_GB_PLAN_CAP=plan-cap-in-gb \
python app.py
```
