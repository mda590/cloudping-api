import boto3
from botocore.client import Config
import os
import urllib
import zipfile
import json

print('Loading function...')

s3 = boto3.client('s3', config=Config(signature_version='s3v4'))
api = boto3.client('apigateway')
pipeline = boto3.client('codepipeline')

def putSuccess(jobId):
    response = pipeline.put_job_success_result(
        jobId=jobId,
        currentRevision={
            'revision': 'rev1',
            'changeIdentifier': 'change1',
        }
    )

def putFailure(jobId, message):
    response = pipeline.put_job_failure_result(
        jobId=jobId,
        failureDetails={
            'type': 'JobFailed',
            'message': message
        }
    )

def lambda_handler(event, context):
    # Get the current job ID for the CodePipeline job calling this function
    jobId = event['CodePipeline.job']['id']
    
    # S3 bucket and key are pulled from the data passed from the previous CodePipeline Action
    bucket = event['CodePipeline.job']['data']['inputArtifacts'][0]['location']['s3Location']['bucketName']
    url = event['CodePipeline.job']['data']['inputArtifacts'][0]['location']['s3Location']['objectKey']
    key = urllib.unquote_plus(url)
    s3_path = os.path.dirname(key)
    
    try:
        # Download the CloudFormation output zip
        # Open the zip file
        s3.download_file(bucket, key, '/tmp/cfoutput.zip')
        zfile = zipfile.ZipFile('/tmp/cfoutput.zip')
        namelist = zfile.namelist()
        data = zfile.read(namelist[0])
        
        # Convert the CF output from string to JSON and grab the API ID
        data = json.loads(data)
        apiId = data['ApiId']
    except Exception as e:
        print(e)
        putFailure(jobId, str(e))
        raise e
    
    try:
        # Create the API GW Base Path Mapping to the correct Custom Domain
        response = api.create_base_path_mapping(
            domainName='api-demo.cloudping.co',
            restApiId=apiId,
            stage='v1',
        )
        putSuccess(jobId)
    except Exception as e:
        print(e)
        putFailure(jobId, str(e))
        raise e
        