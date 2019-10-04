import pika
import json
import os
import requests
import config
import concurrent.futures
import threading
import sys
from collage import Collage


def get_avatars_links(repository):

    for repo_name in repository:
        contributors = requests.get(repository[repo_name]+'?&per_page=100', auth=config.auth)
        if contributors.status_code == 200:
            if not os.path.exists(f'repos/{repo_name}'):
                os.makedirs(f'repos/{repo_name}')
            avatar_links = json.dumps([{repo_name: i['avatar_url']} for i in contributors.json()])
            channel.basic_publish(exchange='', routing_key='download', body=avatar_links)


def avatar_downloader(links):

    for repo_name in links:
        avatar = requests.get(links[repo_name])
        num = links[repo_name].split('/')[-1][:-4]

        # gets image type
        end = avatar.headers['Content-Type'].split('/')[-1]

        with open(f"repos/{repo_name}/avatar{num}.{end}", 'wb') as f:
            f.write(avatar.content)
        print('{}: done'.format(threading.current_thread().name))


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue=sys.argv[1])


def callback_contributors(ch, method, properties, body):
    repositories = json.loads(body)

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(get_avatars_links, repositories)


def callback_download(ch, method, properties, body):
    b = json.loads(body)
    repo = [i for i in b[0]][0]

    with concurrent.futures.ThreadPoolExecutor(max_workers=config.ava_threads) as executor:
        executor.map(avatar_downloader, b)
    channel.basic_publish(exchange='', routing_key='collage', body=repo)


def callback_collage(ch, method, properties, body):
    repo = f'repos/{body.decode("utf-8")}'
    list_of_images = [f'{repo}/{i}' for i in os.listdir(path=repo)]
    Collage(list_of_images)
    channel.basic_publish(exchange='', routing_key='done', body=repo)


if sys.argv[1] == 'contributors':
    channel.basic_consume(
        queue='contributors', on_message_callback=callback_contributors, auto_ack=True)
elif sys.argv[1] == 'download':
    channel.basic_consume(
        queue='download', on_message_callback=callback_download, auto_ack=True)
elif sys.argv[1] == 'collage':
    channel.basic_consume(
        queue='collage', on_message_callback=callback_collage, auto_ack=True)


print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
