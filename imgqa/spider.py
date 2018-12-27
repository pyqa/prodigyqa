"""Module Holds all spider mechanisms using beautiful soup & selenium."""
import csv
from imgqa import BrowserActions


class Webspider(BrowserActions):
    """Holds the Web Spider using selenium fo browser based login."""

    def start_webspider(self, base_url=None, domain=None, csv_file_path=None):
        """Start the webspider using selenium."""
        if base_url and domain and csv_file_path:
            distict_url_set = self._get_distinct_urls(domain, base_url)
            two_page_url_list = self._get_next_layer(domain, distict_url_set)
            three_pageurllist = self._get_next_layer(
                domain, two_page_url_list)
            self._write_to_csv(csv_file_path, three_pageurllist, "w")
            self.driver.quit()

    def _get_next_layer(self, domainname, urlset):
        """Fetch another consecutive layer."""
        pageurl_set = set()
        urllist = list(urlset)
        for url in urllist:
            distict_url_set = self._get_distinct_urls(domainname, url)
            pageurl_set = pageurl_set.union(distict_url_set)
        return pageurl_set

    def _get_distinct_urls(self, domain, url):
        """Remove duplicates and filter for the domain name."""
        self.open(url)
        elementlist = self.driver.find_elements_by_xpath("//*[@href]")
        urllist = []
        for element in elementlist:
            urlval = element.get_attribute("href")
            urllist.append(urlval)
        urlset = set()
        for item in urllist:
            if domain in item:
                urlset.add(item)
        return urlset

    def _write_to_csv(self, fname, urlset, status):
        """Write distinct urls to CSV file."""
        with open(fname, status, newline='') as urllist_file:
            url_writer = csv.writer(urllist_file)
            for val in urlset:
                url_writer.writerow([val])
        urllist_file.close()
