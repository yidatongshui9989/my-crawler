from ccgp_tianjin import TJCrawler as CrawlerTianjin
from ccgp_gov import GovCrawler
from email_helper import EmailHelper
import yaml

with open('email_config.yaml', encoding='utf-8') as f:
    config = yaml.load(f, Loader=yaml.SafeLoader)

crawler_tianjin = CrawlerTianjin()
crawler_gov = GovCrawler()

tem = []
tem.extend(crawler_tianjin.crawl())
tem.extend(crawler_gov.crawl())

email_helper = EmailHelper(config)
email_helper.send_email(tem)