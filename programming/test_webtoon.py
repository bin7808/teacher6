import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'programming.settings')
import django
django.setup()

from webtoon.models import Episode

from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup


def main():
    url_set = { ep.url for ep in Episode.objects.all() }

    episode_list = []

    for page in range(1, 10000):
        params = {
            'titleId': 662774,
            'page': page,
        }
        page_url = 'http://comic.naver.com/webtoon/list.nhn'
        html = requests.get(page_url, params=params).text
        soup = BeautifulSoup(html, 'html.parser')
        for a_tag in soup.select('.viewList .title a'):
            title = a_tag.text
            link = urljoin(page_url, a_tag['href'])

            if link in url_set:
                print('End!')
                return episode_list

            url_set.add(link)

            print(title, link)
            episode_list.append(Episode(title=title, url=link))


if __name__ == '__main__':
    from django.db import connection

    episode_list = main()
    Episode.objects.bulk_create(episode_list)

    for idx, query in enumerate(connection.queries, 1):
        print(idx, query)

