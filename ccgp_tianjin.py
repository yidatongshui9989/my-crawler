import requests
from lxml import etree
import time
from datetime import datetime
from base_crawler import BaseCrawler

class TJCrawler(BaseCrawler):
    def __init__(self):
        super().__init__()
        self.url = "http://ccgp-tianjin.gov.cn/portal/topicView.do"

        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        self.payload = 'method%3A=view'
        self.ids = ['1662', '1994', '1665', '1664', '1663', '1666', '2014', '2013', '2015', '2016', '2021', '2022', '2033', '2034']
        self.rules = {
            'title': './/li//a[@target="_blank"]/@title',
            'link': './/li//a[@target="_blank"]/@href',
            'time': './/span[@class="time"]/text()'
        }

        self.base_url = 'http://ccgp-tianjin.gov.cn/portal/documentView.do?method=view&'


    def _stop_check(self, time_str):
        time_source = datetime.strptime(time_str, '%a %b %d %H:%M:%S CST %Y')
        time_now = datetime.now()
        if (time_now - time_source).days > 3:
            return True
        return False

    def crawl(self):
        targets = []

        for _id in self.ids:
            stop_flag = False
            for page_num in range(1, 20):
                if stop_flag:
                    break

                data = self.payload + f'&page={str(page_num)}' + f'&id={_id}'
                time.sleep(5)
                resp = requests.request('POST', self.url, headers=self.headers, data=data)

                root = etree.HTML(resp.text)
                titles = root.xpath(self.rules['title'])
                links = root.xpath(self.rules['link'])
                open_times = root.xpath(self.rules['time'])

                print(data)

                assert len(titles)==len(links) and len(links)==len(open_times)

                for i in range(len(titles)):
                    title, link, open_time = titles[i], links[i], open_times[i]

                    for t in self.target_contents:
                        if t in title:
                            targets.append(f'{title}： {self.base_url + link.split("?")[-1]}')
                            break

                    stop_flag = self._stop_check(open_time)



        print(targets)
        return targets

