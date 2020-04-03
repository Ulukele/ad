import boto3


def main():


    # Get keys to service account
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')


    # Create client
    client = boto3.client(
        service_name='sqs',
        endpoint_url='https://message-queue.api.cloud.yandex.net',
        region_name='ru-central1',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    # Create queue and get its url
    queue_url = client.create_queue(QueueName='checker-response-queue').get('QueueUrl')
    print('Created queue url is "{}"'.format(queue_url))


    # Receive sent message
    messages = client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,
        VisibilityTimeout=60,
        WaitTimeSeconds=20
    ).get('Messages')
    for msg in messages:
        print('Received message: "{}"'.format(msg.get('Body')))
        print('msg: ', msg)


if __name__ == '__main__':
    main()