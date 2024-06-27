import os
import boto3
import psycopg2
from utils import flatten_json

def get_sqs_messages(queue_url):
    """
    Retrieve messages from the specified SQS queue.

    Params:
    queue_url (str): SQS message URL.

    Returns:
    list: A list of messages retrieved from the SQS queue.
    """
    sqs = boto3.client('sqs', endpoint_url='http://localstack:4566')
    response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=10)
    return response.get('Messages', [])

def write_to_postgres(records):

    """
    Write the provided records to the Postgres database.

    Params:
    records (list): A list of dictionaries of the messages.
    """

    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()
    for record in records:
        cursor.execute(
            """
            INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (record['user_id'], record['device_type'], record['masked_ip'], record['masked_device_id'], record['locale'], record['app_version'], record['create_date'])
        )
    conn.commit()
    cursor.close()
    conn.close()

def main():

    """
    To process messages from SQS and write them to Postgres.
    """

    queue_url = 'http://localhost:4566/000000000000/login-queue'
    messages = get_sqs_messages(queue_url)
    if not messages:
        print("No messages received.")
        return

    records = [flatten_json(message['Body']) for message in messages]
    write_to_postgres(records)
    print("Data written to Postgres.")

if __name__ == '__main__':
    main()
