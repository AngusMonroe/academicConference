from scrapy.spiders import Spider
from scrapy.http import Request
import csv
import re
import urllib
import os

class D23TSpide(Spider):
    # name of the crawler(primary key)
    name = 'D-23T'
    # urls which contain pages you want
    start_urls = ['http://www.cndent.com/archives/category/%E5%AD%A6%E4%BC%9A%E5%8A%A8%E6%80%81/%E9%80%9A%E7%9F%A5%E5%85%AC%E5%91%8A',
                  'http://www.cndent.com/archives/category/%E5%AD%A6%E4%BC%9A%E5%8A%A8%E6%80%81/%E9%80%9A%E7%9F%A5%E5%85%AC%E5%91%8A/page/2',
                  'http://www.cndent.com/archives/category/%E5%AD%A6%E4%BC%9A%E5%8A%A8%E6%80%81/%E9%80%9A%E7%9F%A5%E5%85%AC%E5%91%8A/page/3',
                  'http://www.cndent.com/archives/category/%E5%AD%A6%E4%BC%9A%E5%8A%A8%E6%80%81/%E9%80%9A%E7%9F%A5%E5%85%AC%E5%91%8A/page/4',
                  'http://www.cndent.com/archives/category/%E5%AD%A6%E4%BC%9A%E5%8A%A8%E6%80%81/%E9%80%9A%E7%9F%A5%E5%85%AC%E5%91%8A/page/5',
                  'http://www.cndent.com/archives/category/%E5%AD%A6%E4%BC%9A%E5%8A%A8%E6%80%81/%E9%80%9A%E7%9F%A5%E5%85%AC%E5%91%8A/page/6',
                  'http://www.cndent.com/archives/category/%E5%AD%A6%E4%BC%9A%E5%8A%A8%E6%80%81/%E9%80%9A%E7%9F%A5%E5%85%AC%E5%91%8A/page/7',
                  'http://www.cndent.com/archives/category/%E5%AD%A6%E4%BC%9A%E5%8A%A8%E6%80%81/%E9%80%9A%E7%9F%A5%E5%85%AC%E5%91%8A/page/8',
                  'http://www.cndent.com/archives/category/%E5%AD%A6%E4%BC%9A%E5%8A%A8%E6%80%81/%E9%80%9A%E7%9F%A5%E5%85%AC%E5%91%8A/page/9']

    # callback function
    def parseDetails(self, response):
        # parameters can be got by response.meta['key']
        # url = response.meta['url']

        title = response.xpath('//h1/span/text()')[0].extract()
        content_temp = response.xpath('//div[@class="entry-content"]')[0].extract()

        # use regular expression to resolve the pages you get, especially html elements
        # content_temp = re.sub('<[^>]+>[^<]*</[^>]+>', '', content_temp)
        pattern_h5 = re.compile(r'<[^>]+>', re.S)
        pattern_blackLines = re.compile(r'\n{2,}', re.S)
        content = pattern_blackLines.sub('', pattern_h5.sub('', content_temp))
        content = re.sub('[\t\n\r]', '', content)
        content = re.sub('&nbsp;', '', content)
        content = re.sub(' +', ' ', content)

        # open the file and write and close it
        csvfile = open('output/D-23T.csv', 'a', newline='', errors='ignore', encoding='gbk')
        writer = csv.writer(csvfile)
        writer.writerow([title, content])
        csvfile.flush()
        csvfile.close()

        relative_urls = response.xpath('//a/@href').extract()
        if relative_urls:
            for i in range(len(relative_urls)):
                absolute_url = relative_urls[i]
                # relative_url = relative_urls[i]
                # relative_url = re.sub('<[^>]+>', '', relative_url)
                # relative_url = re.sub('[\t\n\r]', '', relative_url)
                # absolute_url = re.sub(' +', ' ', relative_url)
                if re.findall("(\S*)\.pdf|(\S*)\.doc", absolute_url):
                    print(absolute_url)
                    name = absolute_url.split('/')
                    if not os.path.exists('file/D-23T/'):
                        os.mkdir('file/D-23T/')
                    print('file/D-23T/' + str(name[len(name) - 1]) + ' ' + absolute_url)
                    urllib.request.urlretrieve(absolute_url, 'file/D-23T/' + str(name[len(name) - 1]))

    def parse(self, response):
        # the rules how to deal with the pages you get
        # learn more about 'xpath' grammar
        conference = response.xpath('//h3[@class="entry-title"]')

        # if the page you want is a secondary page and you can only get their urls, you can collect the urls and then use function Requset()
        urls = []

        for i in range(len(conference)):
            url = conference[i].xpath('.//a/@href').extract()[0]
            urls.append(url)

        # print(urls)

        for url in urls:
            # parameters can be passed by meta={'key':value}
            yield Request(url, meta={'url': url}, callback=self.parseDetails)
            # urllib.request.urlretrieve(url, 'filePath/fileName.xxx')