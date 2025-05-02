import os
import json
import uuid
from flask import Flask, request, abort, jsonify
from ibm_boto3 import client
from ibm_botocore.config import Config
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('./ibmcloud.env')

#COS credentials
COS_ENDPOINT = os.getenv('COS_ENDPOINT')
COS_API_KEY_ID = os.getenv('COS_API_KEY_ID')
COS_INSTANCE_CRN = os.getenv('COS_SERVICE_CRN')
COS_BUCKET_NAME = os.getenv('COS_BUCKET_NAME')
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')

# Starting up COS client
cos_client = client(
    service_name='s3',
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_INSTANCE_CRN,
    config=Config(signature_version='oauth'),
    endpoint_url=COS_ENDPOINT
)

# Initialize Flask app
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Verify the webhook secret
    auth_header = request.header.get('Authorization')
    if not auth_heder or auth_header != f'Bearer {WEBHOOK_SECRET}':
        abort(401, description='Unauthorized: Invalid webhook secret')

    # Get data from the webhook
    data = request.get_json()
    if not data:
        abort(400, description='Bad Request: No JSON payload')

    # Generate a unique filename
    file_name = f"log_{uuid.uuid4()}.json"
    
    # Converting the data to JSON Format
    file_data = json.dumps(data, indent=2)

    try:
        #Upload file to the COS bucket
        cos_client.put_object(
            Bucket=COS_BUCKET_NAME, 
            Key=file_name,
            Body=file_data
        )
        return '', 200
    except Exception as e:
        print(f"Error uploading file to COS: {e}")
        abort(500, decription='Internal Server Error')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
