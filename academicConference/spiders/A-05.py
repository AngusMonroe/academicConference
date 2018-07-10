from scrapy.spiders import Spider
from scrapy.http import Request
import csv
import re
import urllib

class A05Spide(Spider):
    # name of the crawler(primary key)
    name = 'A-05'
    # urls which contain pages you want
    start_urls = ['http://www.aschina.org/xshd/index.jhtml',
                  'http://www.aschina.org/xshd/index_2.jhtml',
                  'http://www.aschina.org/xshd/index_3.jhtml']

    # callback function
    def parsecontent_temps(self, response):
        # parameters can be got by response.meta['key']
        # url = response.meta['url']

        title = response.xpath('//div[@class="center_neir"]/text()')[0].extract()
        content_temp = response.xpath('//div[@class="center_neirei"]')[0].extract()

        # use regular expression to resolve the pages you get, especially html elements
        content_temp = re.sub('<[^>]+>', '', content_temp)
        content_temp = re.sub('[\t\n\r]', '', content_temp)
        content_temp = re.sub(' +', ' ', content_temp)

        # open the file and write and close it
        csvfile = open('output/A-05.csv', 'a', newline='', errors='ignore', encoding='gbk')
        writer = csv.writer(csvfile)
        writer.writerow([title, content_temp])
        csvfile.flush()
        csvfile.close()

    def parse(self, response):
        # the rules how to deal with the pages you get
        # learn more about 'xpath' grammar
        conference = response.xpath('//td[@width="576"]').re("<a href=\"([^\"]*)\"")
        print(conference)


        # if the page you want is a secondary page and you can only get their urls, you can collect the urls and then use function Requset()
        urls = []

        for i in range(len(conference)):
            url = 'http://www.aschina.org' + conference[i]  # conference[i].xpath('//a/@href').extract()[0]
            print(url)
            urls.append(url)
        for url in urls:
            # parameters can be passed by meta={'key':value}
            yield Request(url, meta={'url': url}, callback=self.parsecontent_temps)
            # urllib.request.urlretrieve(url, 'filePath/fileName.xxx')
