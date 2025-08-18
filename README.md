## AI Agent with Bedrock, Pinecone, and Serverless API

This project provides a complete, production-ready backend for an AI agent powered by Amazon Bedrock. The agent leverages a Bedrock Knowledge Base with a Pinecone vector store to answer questions based on documents you provide in an S3 bucket.

The entire infrastructure is defined using the AWS Serverless Application Model (SAM) and is deployed automatically via a secure GitHub Actions CI/CD pipeline.

## Architecture

The architecture is fully serverless and event-driven. The CI/CD pipeline automates the deployment of the AWS resources.

GitHub Actions (CI/CD): Pushing to the main branch triggers the deployment workflow.

AWS CloudFormation: The workflow deploys the template.yaml file, provisioning all AWS resources.

API Gateway (HTTP API): Provides a public, serverless REST endpoint.

AWS Lambda: The core function that receives API requests and securely invokes the Bedrock Agent.

Amazon Bedrock Agent: Orchestrates the interaction, using a foundation model to understand the user's prompt.

Bedrock Knowledge Base: The agent queries the knowledge base to find relevant information.

Pinecone: The vector store that enables fast, semantic search over your documents.

Amazon S3: The bucket where you upload your source documents (e.g., PDFs, TXT files) for the knowledge base.

AWS Secrets Manager: Securely stores the Pinecone API key for the knowledge base to use.

IAM Roles: Provide fine-grained, least-privilege permissions for each service to interact securely.

## Prerequisites

- AWS Account
- AWS CLI configured
- Python 3.9+
- A Pinecone account and API key

## Features

Fully Automated Deployment: CI/CD pipeline using GitHub Actions for hands-off deployments.

Infrastructure as Code (IaC): All AWS resources are defined in a single SAM/CloudFormation template.

Secure by Design: Uses AWS Secrets Manager for API keys and secure OIDC authentication between GitHub and AWS.

Scalable & Serverless: Built entirely on managed AWS services that scale automatically.

RAG Enabled: Implements the Retrieval-Augmented Generation pattern using Bedrock Knowledge Base and Pinecone.

Ready for Frontend: Includes CORS configuration in the API Gateway for easy integration with a web application.

## Deployment

This project is deployed automatically. The following setup is required one time.

### Step 1: Fork and Clone the Repository

First, get a copy of the project and navigate into the directory.

git clone https://github.com/Ayoung9598/agent-on-aws.git
cd agent-on-aws

### Step 2: Configure GitHub Secrets

For the deployment workflow to authenticate securely, you must add the following secrets to your GitHub repository settings under Settings > Secrets and variables > Actions:

AWS_ACCOUNT_ID: Your 12-digit AWS Account ID.

AWS_REGION: The AWS region you want to deploy to (e.g., us-east-1).

PINECONE_CONNECTION_STRING: The full connection string for your Pinecone index.

PINECONE_API_KEY: Your secret Pinecone API key.

### Step 3: Configure AWS to Trust GitHub

You must set up an OIDC connection in your AWS account to allow the GitHub Actions workflow to assume a role and deploy resources. Follow the official AWS guide for configuring OIDC with GitHub Actions.

Key Points:

The IAM Role you create in AWS must be named GitHubAction-AIAgent-DeployRole to match the workflow file.

This role needs permissions to deploy the resources in the template.yaml file (CloudFormation, S3, Bedrock, Lambda, IAM, etc.).

### Step 4: Push to main

Once the secrets and the AWS role are configured, every git push to the main branch will automatically trigger the GitHub Actions workflow to build and deploy your application.

## After Deployment: Using Your Agent

Find Your S3 Bucket: Go to the AWS CloudFormation console, select the AIAgent-Stack, and look in the Outputs tab for the KnowledgeBaseS3BucketName.

Upload Documents: Upload your knowledge documents (PDFs, TXT, etc.) to this S3 bucket.

Sync Knowledge Base: In the Amazon Bedrock console, navigate to Knowledge Bases, select the one created by the stack, and click Sync to ingest your new documents.

Call the API: Use the ApiEndpoint URL from the CloudFormation outputs to interact with your agent.

## API Usage

Send a POST request to the /invoke endpoint with the user's prompt.

Example curl command:

curl -X POST \
 https://<api-id>.execute-api.<region>.amazonaws.com/invoke \
 -H 'Content-Type: application/json' \
 -d '{"prompt": "What are the key features of this product?"}'

## Local Development and Testing

You can test your Lambda function locally without deploying. This provides a rapid feedback loop for code changes.

Prerequisites:

AWS SAM CLI

Docker Desktop (must be running)

Steps:

Deploy Once: You must have successfully deployed the stack to AWS at least once, as local testing makes a live call to the already-existing Bedrock agent.

Create a Test Event: Create a file named event.json in the project root with a sample API Gateway request:

{
"body": "{\"prompt\": \"What is your primary function?\"}"
}

Invoke Locally: In VS Code, open the template.yaml file. The AWS Toolkit extension will provide clickable [Invoke Locally] and [Debug Locally] links directly above the ApiFunction resource. Click one to run your function. The output will appear in your terminal.

## Contact

If you have any questions, suggestions, or feedback, please feel free to contact the project owner at [abiolateslim1@gmail.com](mailto:abiolateslim1@gmail.com)
