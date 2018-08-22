from scrapy.spiders import Spider
from scrapy.http import Request
import csv
import re
import urllib
import os

class D24TSpide(Spider):
    # name of the crawler(primary key)
    name = 'D-24T'
    # urls which contain pages you want
    start_urls = ['http://www.caderm.org/servicenews.aspx?id=14']

    # callback function
    def parseDetails(self, response):
        # parameters can be got by response.meta['key']
        # url = response.meta['url']
        print(response)

        title = response.xpath('//div/div/div/text()').extract()[0]
        content_temp = response.xpath('//div/div/div、text()').extract()[1]

        # use regular expression to resolve the pages you get, especially html elements
        # content_temp = re.sub('<[^>]+>[^<]*</[^>]+>', '', content_temp)
        pattern_h5 = re.compile(r'<[^>]+>', re.S)
        pattern_blackLines = re.compile(r'\n{2,}', re.S)
        content = pattern_blackLines.sub('', pattern_h5.sub('', content_temp))
        content = re.sub('[\t\n\r]', '', content)
        content = re.sub('&nbsp;', '', content)
        content = re.sub(' +', ' ', content)

        # open the file and write and close it
        csvfile = open('output/D-24T.csv', 'a', newline='', errors='ignore', encoding='gbk')
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
                    if not os.path.exists('file/D-24T/'):
                        os.mkdir('file/D-24T/')
                    print('file/D-24T/' + str(name[len(name) - 1]) + ' ' + absolute_url)
                    urllib.request.urlretrieve(absolute_url, 'file/D-24T/' + str(name[len(name) - 1]))

    def parse(self, response):
        # the rules how to deal with the pages you get
        # learn more about 'xpath' grammar
        conference = response.xpath('//td[@style="text-decoration:underline;"]/a/@href').extract()
        # print(conference)

        # if the page you want is a secondary page and you can only get their urls, you can collect the urls and then use function Requset()
        urls = []

        for i in range(len(conference)):
            url = 'http://www.caderm.org/' + conference[i]
            urls.append(url)

        print(urls)

        for url in urls:
            # parameters can be passed by meta={'key':value}
            yield Request(url, meta={'url': url}, callback=self.parseDetails)
            # urllib.request.urlretrieve(url, 'filePath/fileName.xxx')
