import boto3

requestst = ({'ip':'ip', 'port':'port', 'round':'round'},)

def main():


    # Create client
    client = boto3.client(
        service_name='sqs',
        endpoint_url='https://message-queue.api.cloud.yandex.net',
        region_name='ru-central1'
    )

    
    # Create queue and get its url
    queue_url = client.create_queue(QueueName='checker-queue').get('QueueUrl')
    print('Created queue url is "{}"'.format(queue_url))

    for req in requestst:
        # Send message to queue
        client.send_message(
            QueueUrl=queue_url,
            MessageBody='{},{},{}'.format(req['ip'],req['port'],req['round'])
        )
        print('Successfully sent message to queue')

if __name__ == '__main__':
    main()