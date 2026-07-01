# 🚀 Serverless Event-Driven ETL Pipeline on AWS

<p align="center">
  <img src="docs/architecture.png" alt="Architecture Diagram" width="100%">
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-FF9900?logo=awslambda)
![Amazon S3](https://img.shields.io/badge/Amazon-S3-569A31?logo=amazons3)
![Amazon DynamoDB](https://img.shields.io/badge/AWS-DynamoDB-4053D6?logo=amazondynamodb)
![GitHub Actions](https://img.shields.io/badge/CI-GitHub_Actions-2088FF?logo=githubactions)
![AWS CodePipeline](https://img.shields.io/badge/CD-CodePipeline-FF4F8B)

</p>

## 📖 Overview

This project demonstrates a **production-style Serverless Event-Driven ETL Pipeline** built entirely on AWS.

The pipeline extracts data from multiple public APIs, uploads raw JSON files into **Amazon S3**, automatically triggers **AWS Lambda** for transformation and validation, and stores the cleaned records in **Amazon DynamoDB**.

The entire project is integrated with **GitHub Actions** and **AWS CodePipeline** to automatically validate code changes and support continuous integration.

---

# ✨ Features

- Fully Serverless Architecture
- Event-Driven ETL Pipeline
- Multiple Data Sources
- Automatic S3 Event Trigger
- Data Cleaning & Validation
- DynamoDB Storage
- CloudWatch Monitoring
- GitHub Actions CI
- AWS CodePipeline
- AWS CodeBuild Validation
- Production-ready Folder Structure

---

# 🏗 AWS Services Used

| Service | Purpose |
|----------|----------|
| Amazon S3 | Store raw JSON files |
| AWS Lambda | Transform & Validate data |
| Amazon DynamoDB | Store cleaned records |
| Amazon CloudWatch | Logs & Monitoring |
| AWS IAM | Permissions |
| GitHub Actions | Continuous Integration |
| AWS CodePipeline | Deployment Pipeline |
| AWS CodeBuild | Build & Validation |

---

# 📂 Project Structure

```
serverless-etl-pipeline/
│
├── docs/
│   ├── architecture.png
│   ├── lambda.png
│   ├── s3.png
│   ├── dynamodb.png
│   ├── cloudwatch.png
│   ├── codepipeline.png
│   └── github-actions.png
│
├── sample_data/
│
├── lambda/
│   ├── earthquake/
│   ├── weather/
│   └── products/
│
├── .github/
│   └── workflows/
│
├── fetch_data.py
├── buildspec.yml
├── requirements.txt
└── README.md
```

---

# 🔄 ETL Workflow

```
Public APIs
      │
      ▼
Python Fetch Script
      │
      ▼
Amazon S3
      │
      ▼
S3 ObjectCreated Event
      │
      ▼
AWS Lambda
      │
      ▼
Validation & Transformation
      │
      ▼
Amazon DynamoDB
      │
      ▼
CloudWatch Logs
```

---

# 📊 Data Sources

| Dataset | API |
|----------|-----|
| 🌍 Earthquake | USGS API |
| 🌦 Weather | Open-Meteo API |
| 🛒 Products | DummyJSON API |

---

# 🚀 CI/CD Pipeline

```
GitHub
     │
     ▼
GitHub Actions
     │
     ▼
AWS CodePipeline
     │
     ▼
AWS CodeBuild
     │
     ▼
Deployment Validation
```

---

# 📸 Project Screenshots

## 🏗 Architecture

![](docs/architecture.png)

---

## 📦 Amazon S3 Bucket

![](docs/s3.png)

---

## ⚡ AWS Lambda Functions

![](docs/lambda.png)

---

## 🗄 DynamoDB Tables

![](docs/dynamodb.png)

---

## 📊 CloudWatch Logs

![](docs/cloudwatch.png)

---

## 🚀 AWS CodePipeline

![](docs/codepipeline.png)

---

## ✅ GitHub Actions

![](docs/github-actions.png)

---

# ▶️ Run Locally

Clone the repository

```bash
git clone https://github.com/yourusername/serverless-etl-pipeline.git
```

Move into project

```bash
cd serverless-etl-pipeline
```

Install dependencies

```bash
pip install -r requirements.txt
```

Fetch sample data

```bash
python fetch_data.py
```

Upload generated JSON files to the configured Amazon S3 bucket to trigger the ETL pipeline.

---

# 📈 Future Improvements

- AWS Step Functions
- SNS Notifications
- Dead Letter Queue (DLQ)
- Terraform Infrastructure
- AWS Glue Integration
- Redshift Data Warehouse
- Unit Testing
- Monitoring Dashboard

---

# 🛠 Tech Stack

- Python 3.12
- AWS Lambda
- Amazon S3
- Amazon DynamoDB
- AWS IAM
- Amazon CloudWatch
- GitHub Actions
- AWS CodePipeline
- AWS CodeBuild
- JSON
- Requests

---

# 👨‍💻 Author

**Anuj Kumar Yadav**

B.Tech Computer Science Engineering

Data Engineering Enthusiast

GitHub: https://github.com/Anuj857

---

## ⭐ If you found this project helpful, consider giving it a Star!