import json
import boto3
import os
import telebot


def handler(event, context):
    ACCESS_KEY = os.environ['ACCESS_KEY']
    SECRET_KEY = os.environ['SECRET_KEY']
    DB_BUCKET = os.environ['DB_BUCKET']
    DB_MESSAGE_OBJECT = os.environ['DB_MESSAGE_OBJECT']
    DB_NAME_OBJECT = os.environ['DB_NAME_OBJECT']
    IMAGES_BUCKET_ID = os.environ['IMAGES_BUCKET_ID']
    TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
    CHAT_ID = int(os.environ['CHAT_ID'])

    s3 = boto3.resource(service_name='s3', endpoint_url='https://storage.yandexcloud.net',
                        aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

    data = json.loads(event["body"])
    message = data['message']
    message_text = message['text']

    if 'entities' in message:
        entities = message['entities']
        splited_message = message_text.split(maxsplit=1)
        if (entities[0]['type'] == 'bot_command') and (splited_message[0] == "/find"):
            b_names = download_file_like_object(s3, DB_BUCKET, DB_NAME_OBJECT)
            dic_names = json.loads(b_names)
            name = splited_message[1]
            paths = get_images_path(name, dic_names)
            send_info_by_name(TELEGRAM_TOKEN, CHAT_ID, name, paths, s3, IMAGES_BUCKET_ID)

    if 'reply_to_message' in message:

        repl_message_id = message['reply_to_message']['message_id']
        b_dic = download_file_like_object(s3, DB_BUCKET, DB_MESSAGE_OBJECT)
        b_names = download_file_like_object(s3, DB_BUCKET, DB_NAME_OBJECT)

        dic = json.loads(b_dic)
        names = json.loads(b_names)

        if str(repl_message_id) in dic:
            object_id = dic[str(repl_message_id)]
            add_name(message_text, object_id, names)
            j = json.dumps(names)
            newFile = s3.Object(DB_BUCKET, DB_NAME_OBJECT)
            newFile.put(Body=j)

    return {
        'statusCode': 200,
        'body': 'OK!',
    }


def download_file_like_object(s3, bucketId, objectId):
    response = s3.Object(bucketId, objectId).get()
    print(response)
    return response['Body'].read()


def add_name(name, object_id, d):
    if name in d:
        if object_id not in d[name]:
            new_list = d[name]
            new_list.append(object_id)
    else:
        d[name] = [object_id]


def get_images_path(name, d):
    if name in d:
        return d[name]
    else:
        return []


def send_info_by_name(token, chat_id, name, object_list, s3, bucketId):
    if len(object_list) == 0:
        message = "Фотографии с " + name + " не найдены"
        tb = telebot.TeleBot(token)
        tb.send_message(chat_id, message)
    else:
        for object_id in object_list:
            b = download_file_like_object(s3, bucketId, object_id)
            tb = telebot.TeleBot(token)
            tb.send_photo(chat_id, b)
