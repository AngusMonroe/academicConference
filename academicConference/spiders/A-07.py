from scrapy.spiders import Spider
from scrapy.http import Request
import csv
import re
import urllib

class A07Spide(Spider):
    # name of the crawler(primary key)
    name = 'A-07'
    # urls which contain pages you want
    start_urls = ['http://astronomy.pmo.cas.cn/xsjl/gnxsjl/',
                  'http://astronomy.pmo.cas.cn/xsjl/gjxsjl/']

    def parse(self, response):
        # the rules how to deal with the pages you get
        # learn more about 'xpath' grammar
        title = response.xpath('.//div[@class="list_list"]/ul/li').re("title=\"([^\"]*)\">")
        url = response.xpath('.//div[@class="list_list"]/ul/li').re("<a href=\"([^\"]*)\"")

        # open file and write
        csvfile = open('output/A-07.csv', 'a', newline='', errors='ignore', encoding='gbk')
        writer = csv.writer(csvfile)

        for i in range(max(len(title), len(url))):
            t = ''
            if title[i]:
                title[i] = re.sub('<[^>]+>', '', title[i])
                t = title[i]

            u = ''
            if url[i]:
                url[i] = re.sub('<[^>]+>', '', url[i])
                url[i] = re.sub('[\t\n\r]', '', url[i])
                url[i] = re.sub(' +', ' ', url[i])
                u = url[i]

            # write to file
            writer.writerow([t, u])

        # close the file
        csvfile.flush()
        csvfile.close()
