# Cloud Resume Challenge

A serverless resume website built on AWS — static frontend served via CloudFront, with a live visitor counter powered by API Gateway, Lambda (Python), and DynamoDB. All infrastructure provisioned as code with Terraform, deployments automated via GitHub Actions CI/CD.

**Live:** [d108sjaxcdd5os.cloudfront.net](https://d108sjaxcdd5os.cloudfront.net)

## Architecture

```
Browser
  │
  ├── HTTPS request
  ▼
CloudFront (CDN + HTTPS)
  │
  ▼
S3 (static hosting)
  │  index.html, CSS, JS
  │
  └── JavaScript fetch() → API Gateway → Lambda (Python) → DynamoDB
                           (POST /count)   (visitor_counter-tf)  (visitor-count-tf)
```

**Frontend:** Static HTML/CSS/JS hosted on S3, served globally via CloudFront with HTTPS.

**Backend:** Serverless visitor counter — every page load triggers a POST to API Gateway, which invokes a Lambda function that increments and returns the count from DynamoDB.

**Infrastructure:** All AWS resources provisioned with Terraform. Deployments triggered automatically on every push to `main`.

## Stack

| Layer | Service |
|---|---|
| CDN + HTTPS | AWS CloudFront |
| Static hosting | AWS S3 |
| API | AWS API Gateway (HTTP API) |
| Compute | AWS Lambda (Python 3.12) |
| Database | AWS DynamoDB (PAY_PER_REQUEST) |
| IaC | Terraform |
| CI/CD | GitHub Actions |
| Tests | Python pytest |

## Project structure

```
cloud-resume/
├── frontend/
│   └── index.html          ← resume (HTML/CSS/JS, visitor counter fetch)
├── backend/
│   ├── lambda_function.py  ← visitor counter logic (Python/boto3)
│   └── test_lambda.py      ← unit tests (pytest, 3/3 passing)
└── terraform/
    ├── main.tf             ← all AWS resources
    └── outputs.tf          ← api_url, dynamodb_table, lambda_function
```

## CI/CD

Two GitHub Actions workflows run on every push to `main`:

**Frontend pipeline** (`frontend.yml`)
- Syncs `frontend/index.html` to S3
- Invalidates CloudFront cache so changes go live immediately

**Backend pipeline** (`backend.yml`)
- Runs Python unit tests with pytest
- Deploys updated Lambda function if tests pass

## Terraform resources

```
aws_s3_bucket                    → static website hosting
aws_cloudfront_distribution      → CDN + HTTPS
aws_apigatewayv2_api             → HTTP API (visitor-counter-api-tf)
aws_apigatewayv2_route           → POST /count
aws_lambda_function              → visitor-counter-tf (Python 3.12)
aws_dynamodb_table               → visitor-count-tf (PAY_PER_REQUEST)
aws_iam_role                     → visitor-counter-role-tf
aws_iam_role_policy_attachment   → DynamoDB + CloudWatch Logs access
aws_lambda_permission            → API Gateway → Lambda invoke
```

## Running locally

```bash
# Preview the resume
open frontend/index.html

# Run backend tests
cd backend
pip install boto3 pytest
pytest test_lambda.py -v

# Deploy infrastructure
cd terraform
terraform init
terraform apply
```

## What I learned

- **Serverless architecture in practice** — connecting API Gateway → Lambda → DynamoDB without managing any servers, and understanding where each piece fits (routing, compute, persistence)
- **CloudFront cache invalidation** — without it, S3 updates don't reach users; the CI/CD pipeline automates this on every deploy
- **Terraform for serverless** — provisioning Lambda, API Gateway routes and integrations, and DynamoDB tables as code felt very different from EC2/VPC work, but the same `plan → apply → destroy` cycle applies
- **CORS configuration** — the API Gateway needed explicit CORS headers to allow the browser to call a different domain; this surfaced during testing when the counter silently failed

## What's next

This project is part of a larger portfolio progression:

```
Cloud Resume (this repo)
    ↓
Hybrid Infrastructure Platform  →  multi-tier VPC, RDS, Node.js API, CloudWatch
    ↓
Dockerized Fullstack Platform   →  Docker, Compose, CI/CD to Docker Hub + ECR
    ↓
Fullstack AWS Deployment        →  Terraform + Docker + EC2 + ECR
    ↓
Kubernetes Series               →  12 labs + 2 projects (kubernetes-mastery-labs)
    ↓
[Planned] Cloud Resume K8s Edition  →  https://cloudresumechallenge.dev/docs/extensions/kubernetes-challenge/
    ↓
[Planned] Final Master Project  →  Terraform + Docker + Kubernetes + AWS EKS
```

The [Kubernetes Challenge extension](https://cloudresumechallenge.dev/docs/extensions/kubernetes-challenge/) of this project — migrating the resume infrastructure to Kubernetes on EKS — is planned as a follow-up after the Kubernetes project series is complete.

## Related projects

- [terraform-learning-labs](https://github.com/tevfikkoyun/terraform-learning-labs) — 12 progressive Terraform labs this project's IaC practices build on
- [hybrid-infra-platform](https://github.com/tevfikkoyun/hybrid-infra-platform) — more complex multi-tier AWS infrastructure with the same Terraform approach
- [kubernetes-mastery-labs](https://github.com/tevfikkoyun/kubernetes-mastery-labs) — 12-lab Kubernetes series, foundation for the planned K8s extension of this project
