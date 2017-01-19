# AWS Inter-Region Latency Monitoring

## Records inter-region latency over a TCP connection between all AWS regions.

### About this Project
This is a sandbox for automating the deployment of the API portion of cloudping.co. For the repository of code currently live,
please visit my cloudping.co repository on GitHub.

Over time, as I've worked on global AWS deployments, I have often been faced with the question of which inter-region transactions will be faced with the most latency.
I have been able to find a lot of static examples of previous testing completed, or anecdotal thoughts based on a region's location. I haven't been able to find any kind of dynamic, consistently updated, latency monitoring.
The goal here is to provide a single source of truth for inter-region AWS region latency.

### How data is collected
* The latency test is performed using the Node.JS "tcp-ping" package (https://www.npmjs.com/package/tcp-ping). The tests are executed against the DynamoDB endpoint URL in each region, on TCP port 443.
* Every region performs a test every 6 hours (0000, 0600, 1200, 1800 UTC) by "pinging" every region's DynamoDB endpoint. The data is then stored in a DynamoDB database for later access.
* For regions with Lambda, the Node.JS code is stored in a Lambda function and executed by a CloudWatch Event calling the Lambda function at the specific times.
* For regions without Lambda, the Node.JS code runs on an EC2 instance, and is scheduled via a cron job every 6 hours. A Lambda function ensures that these EC2 instances are powered on 1 hour prior to test execution, and are shut down within 1 hour after the test executes.

### How to access the data
* Website: You can access a summary of the data at the following location:  https://www.cloudping.co. Note, the table on this page is based on the averages for tests performed in the previous 24-hours.
* API documentation is available here: https://www.cloudping.co/apidocs.

#### Additional Notes
This project is in no way associated with Amazon or AWS. If you wish to report any issues with the project, please use the "Issues" feature within GitHub.