import json
import boto3
import os
import telebot


def handler(event, context):
    print(event)
    ACCESS_KEY = os.environ['ACCESS_KEY']
    SECRET_KEY = os.environ['SECRET_KEY']
    DB_BUCKET = os.environ['DB_BUCKET']
    DB_OBJECT = os.environ['DB_OBJECT']

    TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
    CHAT_ID = int(os.environ['CHAT_ID'])

    s3 = boto3.resource(service_name='s3', endpoint_url='https://storage.yandexcloud.net',
                        aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

    data = event['messages'][0]
    if data['event_metadata']['event_type'] == 'yandex.cloud.events.messagequeue.QueueMessage':
        j_data = data['details']['message']['body']
        j = json.loads(j_data)
        print(j)
        bucket_id = j['bucketId']
        object_id = j['objectId']

        b = download_file_like_object(s3, bucket_id, object_id)
        message_id = send_message_to_user(TELEGRAM_TOKEN, CHAT_ID, b, object_id)
        b_dic = download_file_like_object(s3, DB_BUCKET, DB_OBJECT)
        dic = json.loads(b_dic)
        dic[message_id] = object_id
        j = json.dumps(dic)
        newFile = s3.Object(DB_BUCKET, DB_OBJECT)
        newFile.put(Body=j)

    return {
        'statusCode': 200,
        'body': 'OK!',
    }


def download_file_like_object(s3, bucketId, objectId):
    response = s3.Object(bucketId, objectId).get()
    return response['Body'].read()


def send_message_to_user(token, chat_id, img, object_id):
    tb = telebot.TeleBot(token)
    message = "Кто это?"
    return tb.send_photo(chat_id, img, caption=message).message_id
