import json
import boto3
import os
import uuid

# This client will be initialized by the Lambda execution environment
bedrock_agent_runtime = boto3.client('bedrock-agent-runtime')

def lambda_handler(event, context):
    """
    Handles API Gateway requests to invoke the Bedrock Agent.
    This function is designed to be deployed as an AWS Lambda function.
    """
    try:
        # Retrieve agent details from environment variables set by CloudFormation
        agent_id = os.environ['BEDROCK_AGENT_ID']
        agent_alias_id = os.environ['BEDROCK_AGENT_ALIAS_ID']

        # The request body from API Gateway is a JSON string
        body = json.loads(event.get('body', '{}'))
        prompt = body.get('prompt')

        # Basic input validation
        if not prompt:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Input Error: The "prompt" field is required in the request body.'})
            }

        # Each conversation with the agent requires a unique session ID
        session_id = str(uuid.uuid4())

        # Invoke the agent. This sends the user's prompt to Bedrock.
        response = bedrock_agent_runtime.invoke_agent(
            agentId=agent_id,
            agentAliasId=agent_alias_id,
            sessionId=session_id,
            inputText=prompt
        )

        # The agent's response is a stream of events. We need to assemble the final text.
        completion = ""
        for event_chunk in response.get('completion', []):
            chunk = event_chunk.get('chunk', {})
            # The actual text is in the 'bytes' field of the chunk
            completion += chunk.get('bytes', b'').decode('utf-8')

        # Return a successful HTTP response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*' # Allows cross-origin requests for frontend testing
            },
            'body': json.dumps({'response': completion})
        }

    except Exception as e:
        # Log the error for debugging purposes in CloudWatch
        print(f"Error invoking Bedrock agent: {e}")
        
        # Return a generic server error response
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'An internal server error occurred.'})
        }

