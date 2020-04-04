""" this code needs to send check-requests to yandex cloud """

import boto3
import os


requestst = ({'ip':'ip1', 'port':'port1', 'round':'round1'},{'ip':'ip2', 'port':'port2', 'round':'round2'},{'ip':'ip3', 'port':'port3', 'round':'round3'})

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
    queue_url = client.create_queue(QueueName='checker-queue').get('QueueUrl')
    print('Created queue url is "{}"'.format(queue_url))

    for req in requestst:
        # Send message to queue
        client.send_message(
            QueueUrl=queue_url,
            MessageBody='{},{},{}'.format(req['ip'],req['port'],req['round']),
            MessageAttributes={
                        "ip": {
                            "StringValue": str(req['ip']),
                            "DataType": "Number"
                        },
                        "port": {
                            "StringValue": str(req['port']),
                            "DataType": "Number"
                        },
                        "round": {
                            "StringValue": str(req['round']),
                            "DataType": "Number"
                        }
                    }
        )
        print('Successfully sent message to queue with args: ')
        print('ip', req['ip'])
        print('port', req['port'])
        print('round', req['round'])

if __name__ == '__main__':
    main()