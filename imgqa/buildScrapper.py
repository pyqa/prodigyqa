import os


def create_setup_file(start_urls, allowed_domain_urls):

    """ This is a setup file to create setupscrapper.py
     :param start_urls: a string to parse through urls.
     :param allowed_domain_urls: a string to set domain.
     """

    tmp = open("scraper.tmpl", "r")
    setup = open("setup_scrapper.py", "w+")
    setup.write(tmp.read().format(start_urls,allowed_domain_urls))
    setup.close()
    tmp.close()
    os.system('scrapy crawl URLScraper')
