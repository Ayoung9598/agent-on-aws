# AWS Bedrock AI Agent with Serverless API

This project provides a complete backend for an AI agent powered by Amazon Bedrock. It uses a Knowledge Base with an S3 data source and a Pinecone vector store. The agent is exposed via a serverless API using Amazon API Gateway and AWS Lambda. All infrastructure is provisioned using AWS CloudFormation.

## Architecture

- **API Gateway:** Provides an HTTP endpoint to interact with the agent.
- **AWS Lambda:** Contains the business logic to invoke the Bedrock Agent.
- **Amazon Bedrock Agent:** The core AI agent that processes user requests.
- **Amazon Bedrock Knowledge Base:** Provides the agent with domain-specific knowledge.
- **Amazon S3:** Stores the documents for the Knowledge Base.
- **Pinecone:** Acts as the vector store for the Knowledge Base.

## Prerequisites

- AWS Account
- AWS CLI configured
- Python 3.9+
- An S3 bucket for your Knowledge Base data
- A Pinecone account and API key

## Deployment

1.  **Clone the repository:**

    ```bash
    git clone <your-repo-url>
    cd <your-repo-name>
    ```

2.  **Package the Lambda function:**
    _(Instructions on how to create a zip file for the lambda function if it has dependencies)_

3.  **Deploy the CloudFormation stack:**
    ```bash
    aws cloudformation deploy \
      --template-file template.yaml \
      --stack-name my-bedrock-agent-stack \
      --capabilities CAPABILITY_IAM \
      --parameter-overrides \
        PineconeApiKey=<your-pinecone-api-key> \
        PineconeEnvironment=<your-pinecone-environment> \
        PineconeIndexName=<your-pinecone-index-name> \
        KnowledgeBaseBucketName=<your-s3-bucket-name>
    ```

## API Usage

Once deployed, you can interact with the agent via the API Gateway endpoint provided in the CloudFormation stack outputs.

**Endpoint:** `POST /invoke`

**Request Body:**

```json
{
  "prompt": "Your question for the agent"
}

Example with curl:

curl -X POST \
  https://<api-id>.execute-api.<region>[.amazonaws.com/invoke](https://.amazonaws.com/invoke) \
  -H 'Content-Type: application/json' \
  -d '{"prompt": "What are the latest features of Amazon Bedrock?"}'
```
