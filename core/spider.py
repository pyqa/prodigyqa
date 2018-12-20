import csv
from imgqa.core.pageactions import PageActions


class Webspider(PageActions):

    def start_webspider(self, base_url=None, domain=None, csv_file_path=None):
        if base_url is not None and domain is not None and csv_file_path is not None:
            distictUrlSet = self._get_distinct_urls(domain, base_url)
            TwoPageUrlList = self._getNextPageLayerUrls(domain, distictUrlSet)
            ThreePageUrlList = self._getNextPageLayerUrls(
                domain, TwoPageUrlList)
            self._write_to_csv(csv_file_path, ThreePageUrlList, "w")
            self.driver.quit()

    def _getNextPageLayerUrls(self, domainname, UrlSet):
        nextPageUrlSet = set()
        urllist = list(UrlSet)
        for url in urllist:
            distictUrlSet = self._get_distinct_urls(domainname, url)
            nextPageUrlSet = nextPageUrlSet.union(distictUrlSet)
        return nextPageUrlSet

    '''find all urls in a given page'''

    def _get_distinct_urls(self, domain, url):
        self.open(url)
        elementlist = self.driver.find_elements_by_xpath("//*[@href]")
        urlList = []
        for element in elementlist:
            urlval = element.get_attribute("href")
            urlList.append(urlval)
        '''Remove duplicates and filter for the domain name'''
        urlSet = set()
        for item in urlList:
            if domain in item:
                urlSet.add(item)
        return urlSet

    '''Writes the distinct urls to CSV file'''

    def _write_to_csv(self, fname, urlSet, status):
        with open(fname, status, newline='') as urlList_file:
            url_writer = csv.writer(urlList_file)
            for val in urlSet:
                url_writer.writerow([val])
        urlList_file.close()
