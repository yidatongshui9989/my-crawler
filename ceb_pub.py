import requests
from lxml import etree
import time
from datetime import datetime
from base_crawler import BaseCrawler


class CebpubCrawler(BaseCrawler):
    def __init__(self):
        super().__init__()
        self.url = 'https://bulletin.cebpubservice.com/xxfbcmses/search/bulletin.html?dates=300&categoryId=88&showStatus=1&page='

        self.rules = {
            'title': './/table[@class="table_text"]//tr/td[position()=1]//@title',
            'link': './/table[@class="table_text"]//tr/td[position()=1]//@href',
            'time': './/table[@class="table_text"]//tr/td[position()=5]/text()'
        }


    def _stop_check(self, time_str):
        time_source = datetime.strptime(time_str.strip(), '%Y-%m-%d')
        time_now = datetime.now()
        if (time_now - time_source).days > 1:
            return True
        return False

    def _safe_request(self, url):
        resp = requests.get(url, headers={'Host':'bulletin.cebpubservice.com'}, verify=False)
        while resp.status_code == 403:
            print('waiting')
            time.sleep(600)
            resp = requests.get(url, headers={'Host': 'bulletin.cebpubservice.com'}, verify=False)

        return resp

    def crawl(self):
        targets = []

        for page_num in range(1, 500):
            time.sleep(60)
            target_url = self.url + str(page_num)
            resp = self._safe_request(target_url)

            if resp.status_code == 403:
                print('waiting')
                time.sleep(600)

            root = etree.HTML(resp.content)
            titles = root.xpath(self.rules['title'])
            links = root.xpath(self.rules['link'])
            open_times = root.xpath(self.rules['time'])

            print(target_url)
            print(titles)
            assert len(titles) == len(links) and len(links) == len(open_times)

            if len(titles) == 0:
                break

            for i in range(len(titles)):
                if page_num == 0 and i < 5:
                    open_time = open_times[i]
                    if self._stop_check(open_time):
                        continue

                title, link, open_time = titles[i], links[i], open_times[i]

                if self._stop_check(open_time):
                    break

                for t in self.target_contents:
                    if t in title:
                        targets.append(f'{title}： {link[20:-3]}')
                        break

        print(targets)
        return targets

c = CebpubCrawler()
c.crawl()