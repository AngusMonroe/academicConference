from scrapy.spiders import Spider
from scrapy.http import Request
import csv
import re
import urllib
import urllib.response
from urllib.parse import urljoin
import os

class A13Spide(Spider):
    # name of the crawler(primary key)
    name = 'A-13'
    # urls which contain pages you want
    start_urls = ['http://csmpg.gyig.cas.cn/xsjl2017/hytz_134984/index.html',
                  'http://csmpg.gyig.cas.cn/xsjl2017/hytz_134984/index_1.html',
                  'http://csmpg.gyig.cas.cn/xsjl2017/hytz_134984/index_2.html',
                  'http://csmpg.gyig.cas.cn/xsjl2017/hytz_134984/index_3.html',
                  'http://csmpg.gyig.cas.cn/xsjl2017/hytz_134984/index_4.html',
                  'http://csmpg.gyig.cas.cn/xsjl2017/hytz_134984/index_5.html',
                  'http://csmpg.gyig.cas.cn/xsjl2017/hytz_134984/index_6.html',
                  'http://csmpg.gyig.cas.cn/xsjl2017/hytz_134984/index_7.html']

    # callback function
    def parsecontent_temps(self, response):
        title = response.xpath('//p[@class="wztitle"]/text()')[0].extract()
        c1 = response.xpath('//p[@align="justify"]').extract()
        c2 = response.xpath('//font[@size="3"]/span').extract()
        c3 = response.xpath('//div[@class="TRS_Editor"]').extract()
        c3 = response.xpath('//div[@class="textxl nrhei"]').extract()

        content_temp = ''
        for i in c1:
            content_temp += i + ' '
        for i in c2:
            content_temp += i + ' '
        for i in c3:
            content_temp += i + ' '

        content_temp = re.sub('<[^>]+>', '', content_temp)
        content_temp = re.sub('[\t\n\r]', '', content_temp)
        content_temp = re.sub(' +', ' ', content_temp)

        # open the file and write and close it
        csvfile = open('output/A-13.csv', 'a', newline='', errors='ignore', encoding='gbk')
        writer = csv.writer(csvfile)
        writer.writerow([title, content_temp])
        csvfile.flush()
        csvfile.close()

        relative_urls = response.xpath('..//a[@href]').re("<a href=\"([^\"]*)\"")
        if relative_urls:
            relative_url = ''
            for i in range(len(relative_urls)):
                relative_url = relative_urls[i]
                relative_url = re.sub('<[^>]+>', '', relative_url)
                relative_url = re.sub('[\t\n\r]', '', relative_url)
                relative_url = re.sub(' +', ' ', relative_url)
                absolute_url = urljoin(response.url, relative_url)
                if re.findall("(\S*)\.pdf|(\S*)\.doc", absolute_url):
                    name = absolute_url.split('/')
                    if not os.path.exists('file/A-13/'):
                        os.mkdir('file/A-13/')
                    print('file/A-13/' + str(name[len(name) - 1]) + ' ' + absolute_url)
                    urllib.request.urlretrieve(absolute_url, 'file/A-13/' + str(name[len(name) - 1]))

    def parse(self, response):
        # the rules how to deal with the pages you get
        # learn more about 'xpath' grammar
        conference = response.xpath('//div[@class="list-tab"]/ul/li/a').re("<a href=\"([^\"]*)\"")

        urls = []

        for i in range(len(conference)):
            conference[i] = re.sub("\./", "", conference[i])
            url = 'http://csmpg.gyig.cas.cn/xsjl2017/hytz_134984/' + conference[i]  # conference[i].xpath('//a/@href').extract()[0]
            print(url)
            urls.append(url)
        for url in urls:
            # parameters can be passed by meta={'key':value}
            yield Request(url, meta={'url': url}, callback=self.parsecontent_temps)
