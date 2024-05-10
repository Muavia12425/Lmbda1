import json
import base64
import boto3
import os
import uuid

def lambda_handler(event, context):
    s3 = boto3.client("s3")
    
    # Get the content from the event
    get_file_content = event.get("content", "")
    
    # Decode the content
    decode_content = base64.b64decode(get_file_content)
    
    # Get the filename from the Content-Disposition header or provide a default filename if not present
    file_name = get_filename_from_content_disposition(event.get("Content-Disposition", ""))
    if not file_name:
        file_name = event.get("filename", "default_filename")
    
    # Generate a unique key (filename) for the uploaded file
    unique_filename = str(uuid.uuid4()) + "_" + file_name
    
    # Upload the file to S3
    s3_upload = s3.put_object(Bucket="lambda-api-upload1", Key=unique_filename, Body=decode_content)

    # Return the response
    return {
        'statusCode': 200,
        'body': json.dumps('The object has been uploaded successfully with filename: {}'.format(unique_filename))
    }

def get_filename_from_content_disposition(content_disposition):
    if content_disposition:
        parts = content_disposition.split(";")
        for part in parts:
            if part.strip().startswith("filename="):
                return part.split("=")[1].strip().strip('"')
    return None
