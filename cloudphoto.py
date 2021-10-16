import boto3
import os
import click


@click.group()
def cli():
    pass


@cli.command()
@click.option('-p')
@click.option('-a')
def upload(p, a):
    if not os.path.exists(os.path.dirname(p)):
        print("Directory not found")
        return
    files = [f for f in os.listdir(p) if os.path.isfile(os.path.join(p, f))]
    for file in files:
        boto3_client.upload_file(os.path.join(p, file).replace("\\", "/"), bucket,
                                 os.path.join(a, file).replace("\\", "/"))


@cli.command()
@click.option('-p')
@click.option('-a')
def download(p, a):
    files = find(a)
    if not list(files.limit(1)):
        print("Album not found")
        return
    for file in files:
        if file.key[-1] == "/":
            continue
        if not os.path.exists(os.path.dirname(p)):
            print("Directory not found")
            return
        path, filename = os.path.split(file.key)
        pathname = os.path.join(p, filename)
        boto3_client.download_file(bucket, file.key, pathname)


def find(a):
    my_bucket = boto3_resource.Bucket(bucket)

    files = my_bucket.objects.filter(Prefix=a, Delimiter='/')
    return files


@cli.command()
@click.option('-a')
def list_files(a):
    files = find(a)
    if not list(files.limit(1)):
        print("Album not found")
        return
    for file in files:
        if file.key[-1] == "/":
            continue
        print(file.key)


@cli.command()
def list_album():
    result = boto3_client.list_objects(Bucket=bucket, Delimiter='/')
    if result.get('CommonPrefixes') is not None:
        for o in result.get('CommonPrefixes'):
            print(o.get('Prefix'))
            list_album_recursive(o.get('Prefix'))


def list_album_recursive(prefix):
    result = boto3_client.list_objects(Bucket=bucket, Prefix=prefix, Delimiter='/')
    if result.get('CommonPrefixes') is not None:
        for o in result.get('CommonPrefixes'):
            print(o.get('Prefix'))
            list_album_recursive(o.get('Prefix'))


if __name__ == '__main__':
    URL = 'https://storage.yandexcloud.net'
    bucket = 'd43.itiscl.ru'
    boto3_client = boto3.client(service_name='s3', endpoint_url=URL)
    boto3_resource = boto3.resource(service_name='s3', endpoint_url=URL)

    cli()
