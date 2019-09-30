import requests
import os
import config
import collage_oop as col


class AvatarsDownloader:
    def __init__(self, search, auth=config.auth):
        self.search = search
        self.api_url = 'https://api.github.com/search/repositories?q='
        self.auth = auth
        self.r = requests.get(f'{self.api_url}{search}',
                              auth=self.auth)
        self.answer = self.r.json()
        self.repos_names = []

    def make_repo_dir(self):
        if len(self.answer['items']) >= 10:
            for e, i in enumerate(self.answer['items'][:10]):
                self.repos_names.append({f"{e+1}_{i['name']}":
                                             i['contributors_url']})
        else:
            for e, i in enumerate(self.answer['items']
                                  [:len(self.answer['items'])]):
                self.repos_names.append({f"{e+1}_{i['name']}":
                                             i['contributors_url']})

    def get_avatars_links(self, contributors, repo_name):
        if contributors.status_code == 200:
            if not os.path.exists(f'repos/{repo_name}'):
                os.makedirs(f'repos/{repo_name}')

            # collects avatar urls from repo contributors
            avatar_links = [i['avatar_url'] for i in contributors.json()]
            return avatar_links
        else:
            print(f'{repo_name} repository has no contributors')

    def avatar_downloader(self, avatar_links, repo_name):
        counter = 1
        for link in avatar_links:
            avatar = requests.get(link)

            # gets image type
            end = avatar.headers['Content-Type'].split('/')[-1]

            with open(f"repos/{repo_name}/avatar{counter}.{end}", 'wb') as f:
                f.write(avatar.content)
            counter += 1

    def run(self):
        self.make_repo_dir()
        for repo in self.repos_names:
            for repo_name in repo:
                contributors = requests.get(repo[repo_name], auth=self.auth)
                self.avatar_downloader(self.get_avatars_links(contributors,
                                                              repo_name),
                                       repo_name)


if __name__ == '__main__':
    AvatarsDownloader(config.search).run()
    list_of_repos = [f'repos/{i}' for i in os.listdir(path="repos")]
    for repo in list_of_repos:
        list_of_images = [f'{repo}/{i}' for i in os.listdir(path=repo)]
        col.Collage(list_of_images, repo).run()
