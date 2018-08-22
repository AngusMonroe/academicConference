from scrapy.spiders import Spider
from scrapy.http import Request
import csv
import re
import urllib

class D20Spide(Spider):
    # name of the crawler(primary key)
    name = 'D-20'
    # urls which contain pages you want
    start_urls = ['http://www.csi.org.cn/class/view?id=22',
                  'http://www.csi.org.cn/class/view?id=22&page=2',
                  'http://www.csi.org.cn/class/view?id=22&page=3']

    # callback function
    def parseDetails(self, response):
        # parameters can be got by response.meta['key']
        # url = response.meta['url']

        title = response.xpath('//h3[@class="atitle"]/text()')[0].extract()
        content_temp = response.xpath('//div[@class="details"]')[0].extract()

        # use regular expression to resolve the pages you get, especially html elements
        pattern_h5 = re.compile(r'<[^>]+>', re.S)
        pattern_blackLines = re.compile(r'\n{2,}', re.S)
        content = pattern_blackLines.sub('', pattern_h5.sub('', content_temp))

        # open the file and write and close it
        csvfile = open('output/D-20.csv', 'a', newline='', errors='ignore', encoding='gbk')
        writer = csv.writer(csvfile)
        writer.writerow([title, content])
        csvfile.flush()
        csvfile.close()

    def parse(self, response):
        # the rules how to deal with the pages you get
        # learn more about 'xpath' grammar
        conference = response.xpath('//div[@class="brief"]')

        # if the page you want is a secondary page and you can only get their urls, you can collect the urls and then use function Requset()
        urls = []

        for i in range(len(conference)):
            url =conference[i].xpath('.//p/a/@href').extract()[0]
            urls.append(url)

        # print(urls)

        for url in urls:
            # parameters can be passed by meta={'key':value}
            yield Request(url, meta={'url': url}, callback=self.parseDetails)
            # urllib.request.urlretrieve(url, 'filePath/fileName.xxx')