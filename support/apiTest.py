import boto3
import urllib2

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

    status = True

    # Connect to Hello API test endpoint
    response = urllib2.urlopen('https://api-demo.cloudping.co/hello')
    html = response.read()
    expected_text = 'Hello World!'

    # Verify that the expected text exists in the index.html page
    if(expected_text not in html):
        status = False

    # Connect to Actual Cloudping Averages Data endpoint
    response = urllib2.urlopen('https://api-demo.cloudping.co/averages')
    html = response.read()
    expected_text = '"region": "ap-south-1"'

    # Verify that the expected text exists in the index.html page
    if(expected_text not in html):
        status = False

    if(status == False):
        message = 'API did not respond or values being served are not expected.'
        print message
        putFailure(jobId, message)
    else:
        print 'API tests succeeded!'
        putSuccess(jobId)
        