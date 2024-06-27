# ETL Application for Fetch Rewards

### Attention Needed: The provided Localstack image had an issue with the request made to the server to read the messages.

Below is the error message I was getting while working on it. This issue is also acknowledged by the developers of the Localstack. That thread can be accessed from here : https://github.com/localstack/localstack/issues/9610

`localstack.aws.protocol.parser.ProtocolParserError: Operation detection failed. Missing Action in request for query-protocol service ServiceModel(sqs) `

To Troubleshoot this issue, I went through Localstack's documentation, but unfortunately could not find the fix.  



## Overview

This application reads JSON data containing user login behavior from an AWS SQS Queue, transforms the data by masking PII fields (`device_id` and `ip`), and writes the transformed data to a PostgreSQL database. 

## Setup and Running the Application

### Prerequisites

- Docker
- Docker Compose
- Python 3.x
- `awscli-local`
- `psql`

### Docker Setup

1. Clone this repository:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Start the Docker containers:

    ```bash
    docker-compose up -d
    ```

### Local Access

1. Verify localstack is running:
    ```bash
    awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/login-queue
    ```

2. Connect to the Postgres database:
    ```bash
    psql -d postgres -U postgres -p 5432 -h localhost -W
    ```

### Running the Script


1. Install Python dependencies:
    ```bash
    pip install boto3 psycopg2-binary
    ```

2. Run the ETL script:
    ```bash
    python etl.py
    ```

## Questions and Answers

### How would you deploy this application in production?

In a production environment, I would deploy this application using container orchestration tools like Kubernetes or AWS ECS. The application could be packaged as a Docker image and deployed to a cluster with auto-scaling capabilities. For database connections, I would use a managed Postgres service like Amazon RDS to ensure scalability and reliability.

### What other components would you want to add to make this production ready?

To make this application production-ready, I would add:
- Logging and monitoring using tools AWS CloudWatch or Datadog services.
- Error handling and retries for failed SQS message processing.
- Security best practices, including IAM roles.
- Backup recovery strategies for the Postgres database.

### How can this application scale with a growing dataset?

The application can scale horizontally by adding more instances of the ETL processor, each reading from the SQS queue. Using a load-balanced Postgres setup can handle increased write operations. For further scaling, sharding or partitioning of the database tables can be considered.

### How can PII be recovered later on?

PII can be recovered by storing the original values in a secure, encrypted database. Each masked value would have a corresponding entry in this store. However, this requires implementing secure key management and access controls.

### What are the assumptions you made?

- The JSON data from the SQS queue is consistent.
- The provided Docker images have the necessary test data and schema set up.
- Masking PII with SHA-256 is sufficient for identifying duplicates and does not require reversibility.

