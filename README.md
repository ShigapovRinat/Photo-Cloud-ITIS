# Commands:
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