import os
import pika
import requests
import config
import json


def collect_repo_dirs(search=config.search):
    api_url = 'https://api.github.com/search/repositories?q='
    auth = config.auth
    r = requests.get(f'{api_url}{search}', auth=auth)
    answer = r.json()
    repos_names = []

    items = answer['items']
    if len(items) < 10:
        for e, i in enumerate(items[:len(items)]):
            repos_names.append({f"{e+1}_{i['name']}": i['contributors_url']})

    for e, i in enumerate(items[:10]):
        repos_names.append({f"{e+1}_{i['name']}": i['contributors_url']})

    return repos_names


repos = json.dumps(collect_repo_dirs(config.search))

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='contributors', auto_delete=False)

channel.basic_publish(exchange='', routing_key='contributors', body=repos)

channel = connection.channel()
channel.queue_declare(queue='done', auto_delete=False)

counter = 0

def callback(ch, method, properties, body):
    global counter
    print("[x] Collage ready for repo: %r" % (body,))
    counter += 1
    if counter == 10:
        channel.basic_publish(exchange='', routing_key='contributors', body='done')
        channel.basic_publish(exchange='', routing_key='download', body='done')
        channel.basic_publish(exchange='', routing_key='collage', body='done')
        connection.close()



channel.basic_consume('done', callback, auto_ack=True)

print("[x] Start consume")
channel.start_consuming()
