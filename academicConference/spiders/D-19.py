from scrapy.spiders import Spider
from scrapy.http import Request
import csv
import re
import urllib

class D19Spide(Spider):
    # name of the crawler(primary key)
    name = 'D-19'
    # urls which contain pages you want
    start_urls = ['http://www.carm.org.cn/Home/Article/lists/category/academic_activities.html']

    # callback function
    def parseDetails(self, response):
        # parameters can be got by response.meta['key']
        # url = response.meta['url']

        title = response.xpath('//h3[@style="text-align:center;"]/text()')[0].extract()
        content_temp = response.xpath('//div[@class="content"]')[0].extract()

        # use regular expression to resolve the pages you get, especially html elements
        pattern_h5 = re.compile(r'<[^>]+>', re.S)
        pattern_blackLines = re.compile(r'\n{2,}', re.S)
        content = pattern_blackLines.sub('', pattern_h5.sub('', content_temp))

        # open the file and write and close it
        csvfile = open('output/D-19.csv', 'a', newline='', errors='ignore', encoding='gbk')
        writer = csv.writer(csvfile)
        writer.writerow([title, content])
        csvfile.flush()
        csvfile.close()

    def parse(self, response):
        # the rules how to deal with the pages you get
        # learn more about 'xpath' grammar
        conference = response.xpath('//li[@class="list_item"]')

        # if the page you want is a secondary page and you can only get their urls, you can collect the urls and then use function Requset()
        urls = []

        for i in range(len(conference)):
            url ='http://www.carm.org.cn'+conference[i].xpath('.//a/@href').extract()[0]
            urls.append(url)
        for url in urls:
            # parameters can be passed by meta={'key':value}
            yield Request(url, meta={'url': url}, callback=self.parseDetails)
            # urllib.request.urlretrieve(url, 'filePath/fileName.xxx')