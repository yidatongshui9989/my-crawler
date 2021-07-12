import requests
from lxml import etree
import time
from datetime import datetime
from base_crawler import BaseCrawler


class GovCrawler(BaseCrawler):
    def __init__(self):
        super().__init__()

        self.base_url = 'http://www.ccgp.gov.cn/cggg/'

        self.urls = [

            'http://www.ccgp.gov.cn/zcdt/index.htm',
            'http://www.ccgp.gov.cn/cggg/dfgg/index.htm',
            'http://www.ccgp.gov.cn/xxgg/qtcgxx/index.htm',
            'http://www.ccgp.gov.cn/cggg/zygg/index.htm'
        ]

        self.rules = {
            'title': './/ul[@class="c_list_bid" or @class="c_list_tat"]/li/a/@title',
            'link': './/ul[@class="c_list_bid" or @class="c_list_tat"]/li/a/@href',
            'time_1': './/ul[@class="c_list_bid"]/li/em[position()=1 or position()=2]/text()',
            'time_2': './/ul[@class="c_list_tat"]/li/span/text()'
        }

    def _stop_check(self, time_str):
        time_source = datetime.strptime(time_str.strip(), '%Y-%m-%d %H:%M')
        time_now = datetime.now()
        if (time_now - time_source).days > 1:
            return True
        return False


    def crawl(self):

        targets = []

        for url in self.urls:
            stop_flag = False
            for page_num in range(100):
                if stop_flag:
                    break

                time.sleep(3)
                target_url = url
                if page_num > 0:
                    target_url = target_url[:-4]
                    target_url = f'{target_url}_{str(page_num)}.htm'
                resp = requests.get(target_url)

                root = etree.HTML(resp.content)
                titles = root.xpath(self.rules['title'])
                links = root.xpath(self.rules['link'])
                open_times = root.xpath(self.rules['time_1'])
                if len(open_times) == 0:
                    open_times = root.xpath(self.rules['time_2'])
                open_times = [open_time for open_time in open_times if '-' in open_time]

                print(target_url)
                assert len(titles) == len(links) and len(links) == len(open_times)

                if len(titles) == 0:
                    stop_flag = True

                for i in range(len(titles)):
                    if page_num == 0 and i < 5:
                        open_time = open_times[i]
                        if self._stop_check(open_time):
                            continue

                    title, link, open_time = titles[i], links[i], open_times[i]

                    for t in self.target_contents:
                        if t in title and not self._stop_check(open_time):
                            tem_1 = f'{title}： {self.base_url + target_url.split("/")[-2] + link[1:]}'
                            if title not in ''.join(targets):
                                targets.append(tem_1)
                            break

                    stop_flag = self._stop_check(open_time)

        print(targets)
        return targets
