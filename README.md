# Задание №1
## Commands:
 * download
    - Закачивает в облоко все файлы
    - Пример команды: python .\cloudphoto.py download -p "C:/Users/pc/PycharmProjects/cloudphoto/test" -a "test1/"
 * list-album
    - Выводит все папки которые есть (включая вложенные)
    - Пример команды: python .\cloudphoto.py list-album
 * list-files
    - Выводит все файлы в папке (не включая вложенные)
    - -a <album> (на конце должен быть '/')
    - Пример команды: python .\cloudphoto.py list-files -a "test1/"
 * upload
    - Закачивает из облока все файлы
    - Пример команды: python .\cloudphoto.py upload -p "C:/Users/pc/PycharmProjects/cloudphoto/test" -a "test1/"

### Креды задаем через ~/.aws/credentials

# Задание №2

В облаке необходимо создать: 
- триггер на создание обьекта; 
- очередь, для записи созданных обьектов
- облачную функцию


Для нахождения координат лиц использовал Face++ 
Фотографии лиц хранятся по пути 'название_альбома/имя_исходного_файла/фото_лица'

### Облачная функция 
#### Переменные окружения
* FACE_SECRET_KEY - секретный ключ от анализотора фото Face++
* FACE_ACCESS_KEY - ключ доступа от анализотора фото Face++
* SECRET_KEY - секретный ключ от сервисного аккаунта Yandex Cloud
* ACCESS_KEY - ключ доступа от сервисного аккаунта Yandex Cloud
* SQS_QUEUE - название очереди
* Точка входа: cloud_function.function


# Задание 3

Функции бота:

* ответ на вопрос: Кто это? через Ответить
* поиск по имени: /find ИМЯ

В Object Storage необходимо создать name.txt и message.txt

## Для функции из папки ask

Создать триггер для очереди из второго задания 
на функцию из этой папки с точкой входа index.handler

#### Переменные окружения
* SECRET_KEY (секретный ключ от аккаунта Yandex Cloud)
* ACCESS_KEY (ключ доступа от аккаунта Yandex Cloud)
* TELEGRAM_TOKEN (токен telegram бота)
* DB_BUCKET (название Object Storage, где находится файл message.txt)
* CHAT_ID (id чата ботом)
* DB_OBJECT (object_id файла message.txt)

## Для функции из папки bot

Добавить telegram Webhook для этого бота на эту облачную функцию
Точка входа: index.handler

#### Переменные окружения
* SECRET_KEY (секретный ключ от аккаунта Yandex Cloud)
* ACCESS_KEY (ключ доступа от аккаунта Yandex Cloud)
* TELEGRAM_TOKEN (токен telegram бота)
* DB_BUCKET (название Object Storage, где находится файл message.txt)
* CHAT_ID (id чата ботом)
* DB_MESSAGE_OBJECT (object_id файла message.txt)
* DB_NAME_OBJECT (object_id файла name.txt)
* IMAGES_BUCKET_ID (название Object Storage, где находятся фотографии)
