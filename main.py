import requests
import os
import config


def download_avatars(search, auth=config.auth):
    r = requests.get(f'https://api.github.com/search/repositories?q={search}',
                     auth=auth)
    answer = r.json()
    repos_names = []
    if len(answer['items']) >= 10:
        for e, i in enumerate(answer['items'][:10]):
            repos_names.append({f"{e+1}_{i['name']}": i['contributors_url']})
    else:
        for e, i in enumerate(answer['items'][:len(answer['items'])]):
            repos_names.append({f"{e+1}_{i['name']}": i['contributors_url']})

    for repo in repos_names:
        for key in repo:
            contributors = requests.get(repo[key], auth=auth)

            if contributors.status_code == 200:
                if not os.path.exists(f'repos/{key}'):
                    os.makedirs(f'repos/{key}')
                avatar_links = [i['avatar_url'] for i in contributors.json()]  # collects avatar urls from repo contributors
                counter = 1
                for link in avatar_links:
                    avatar = requests.get(link)
                    end = avatar.headers['Content-Type'].split('/')[-1]        # gets image type

                    with open(f"repos/{key}/avatar{counter}.{end}", 'wb') as f:
                        f.write(avatar.content)
                    counter += 1
            else:
                print(f'{key} repository has no contributors')


if __name__ == '__main__':
    download_avatars(config.search)
