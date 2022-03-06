
## AWS Batch w/ Docker and Python

This demo project that walks through how to create a batch job using AWS Batch, Docker, Python and Dynamo DB



## Author

- [@SylvesterYiadom](https://www.linkedin.com/in/syyiadom/)


## Tech Stack

**AWS:** Batch, ECR, DynamoDB, IAM

**Others:** Docker, Python


## Documentation


Please reference the files above for Dockerfile and python script used in this demo

## STEP 1 : Create AWS ECR repository for docker image
1. Login to your aws console and navigate to Elastic Container Registry . Click on `Get Started` to create a repository.
2. Give your repository a name and leave all other options as default.  
`Repository name : eg: batch_demo_repo`

3. Create repository
4. Select radio button next to your repository and click on `"View push commands"`
5. Back on your commandline, create a folder and copy Dockerfile and python code provided in this demo
6. Ran commands provided in step 4 to create a docker image and push to ECR. There are commands for both windows and Linux/MacOS systems


## STEP 2 : Create DynamoDB Table to store processed data
1. Back on your aws console, navigate to DynamoDB dashboard , click on create table. Use the following values
    
    `Table name: batch_table (this should match the name given to dynamoDB table instance in the python code)`
    
    `Partition key: pm_key (Number)`

    `Sort key: sc_key (Number)`

    Leave everything else as default and create table

## STEP 3 : Create AWS Batch environment, Queue and Job Definition
1.  Navigate to Batch service and on the left menu click on compute environment. Create a compute environment for your batch job using the following values

    `Compute environment type: Managed`
    
    `Compute environment name: Eg: batch-demo-env`

    `Provisioning model: On-demand`

    `Maximum vCPUs: 256`

    `VPC ID: Select your default VPC ID`

    `Subnets: Select all available subnets in your VPC`

    Create compute environment

## STEP 4 : Create  Job Queue
1.  Create job queue using the follow values

    `Job queue name: Eg: batch-demo-queue`

    `Priority: 100 (The higher the priority number the higher up it will be in the queue to be processed)`

    `Select a compute environment: Select the environment created in step 3 (batch-demo-env) and click Create.`

## STEP 5 : Create job definition
1. Create job definition using the following values

    `Job type: Single-node`

    Under General configuration
    
    `Name: Eg: demo-job-queue`

    `Platform type: EC2`

    `Execution role: ecsTaskExecutionRole`

    `Image`: This should be your docker image URI created in Step 1 (AWS ECR section) . eg: `123456.dkr.ecr.us-east-1.amazonaws.com/batch_demo_repo:latest`

    `Command syntax: Bash`
 
    ```bash
    Command: python /source/batch_upload.py
    ```    
    `vCpus - required: 1`

    `Memory - required: 256`

    `Job role configuration: batchDynamoECSAccess` . Create an IAM role that provides the container in your job with permissions to use the AWS APIs. In this case, ECS task role to make DynamoDB updates.

    Go to `AWS IAM` -> `Roles` -> `Create Role` -> `AWS Service` -> Use cases for other AWS services: `Elastic Container Service` -> `Elastic Container Service Task` -> AmazonDynamoDBFullAccess -> Role name eg: batchDynamoECSAccess > create role



## STEP 6 : Submit new job
1.  Select `Jobs` from the left menu list and create a job using the following values

    `Name: eg: batch-demo-job`

    `Job definition - required`: select from the drop down the definition created from previous step (demo-job-queue:1)

    `Job queue - required: batch-demo-queue`

    Leave everything else as default as it will pull in values from the job definition.

    Click `Submit` to place your job in the queue for processing

2.  Back on your aws batch dashboard your should see 1 Runnable task. The page should refresh every 60 seconds to show your the status of your batch job.

    `Job goes from Submitted -> Pending -> Runnable -> Starting -> Running - either Succeeded or Failed`

    Once the job is complete, you should be able to view it by clicking on Job name and Log stream name hyperlink to show the logs in AWS cloudwatch log groups.

3. To confirm that data was loaded into DynamoDB as scripted in our python code, navigate to `DynamoDB dashboard`
 
    Click on `Tables` , table name (`batch_table`) -> `Explore table items`

    This should show all the data uploaded to the DynamoDB table


## STEP 7 : Clean up

1.  Delete DynamoDB table
2.  Delete ECR repository
3.  Disable Compute environment , Job Queue and Deregister Job Definition
4.  Once disabled delete job queue and compute environment
