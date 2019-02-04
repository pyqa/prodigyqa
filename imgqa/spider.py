"""Module Holds all spider mechanisms using beautiful soup & selenium."""
from imgqa import BrowserActions
from BeautifulSoup import BeautifulSoup
from urlparse import urlparse
import pandas as pd
import os


class Webspider(BrowserActions):
    """Crawl a page and extract all urls recursively within same domain."""

    def spider(self, parent_url, login=False,
               username="", password="", login_button=''):
        """Hold the Web Spider using selenium fo browser based login."""
        self.url = parent_url
        self.url_list = list()
        self.crawled_urls = list()
        self.domain = urlparse(self.url).netloc
        self.url_list.append(self.url)

        self.open(self.url)
        if login:
            if isinstance(username, dict) and isinstance(password, dict) and isinstance(login_button, dict):
                self.send_keys(username)
                self.send_keys(password)
                self.click(login_button)

                # Initiate the crawling by passing the beginning url
                self.crawled_urls, self.url_list = self.__crawl_urls()

                # Load the matched url list to excel
                self.__load_to_excel()
                self.driver.quit()
            else:
                raise AssertionError("credentials are mandatory")
        else:
            tmp = open("..\\imgqa\\setup_scrapper.tmpl", "r")
            setup = open("..\\imgqa\\setup_scrapper.py", "w+")
            setup.write(tmp.read().format(self.url, self.domain))
            setup.close()
            tmp.close()
            os.system('scrapy crawl URLScraper')

    def __crawl_urls(self):
        """Get a set of urls and crawl each url recursively."""
        self.crawled_urls.append(self.url)

        html_source = self.get_page_source()
        html = html_source.encode("utf-8")
        soup = BeautifulSoup(html)
        urls = soup.findAll("a")

        # Even if the url is not part of the same domain, it is still collected
        # But those urls not in the same domain are not parsed
        for a in urls:
            if a.get("href") not in self.url_list:
                self.url_list.append(a.get("href"))

        # Recursively parse each url within same domain
        for page in set(self.url_list):
            if (urlparse(page).netloc == self.domain)\
                    and (page not in self.crawled_urls):
                self.__crawl_urls(self.url_list,
                                  self.crawled_urls, self.driver, page)
        else:
            return self.crawled_urls, self.url_list

    def __load_to_excel(self):
        """Load the list into excel file using pandas."""
        df = pd.DataFrame(self.url_list)

        # So that the excel column starts from 1
        df.index += 1
        path = os.getcwd()
        xlw = pd.ExcelWriter(path + "\\crawler.xlsx")
        df.to_excel(xlw, sheet_name="URLs",
                    index_label="S.NO", header=["URL"])
        xlw.save()
