from scrapy.spiders import Spider
from scrapy.http import Request
import csv
import re
import urllib
import urllib.response
import os

class A08Spide(Spider):
    # name of the crawler(primary key)
    name = 'A-08'
    # urls which contain pages you want
    start_urls = ['http://www.cms1924.org/WebPage/WebPage_75_108.aspx',
                  'http://www.cms1924.org/WebPage/WebPage_75_109.aspx',
                  'http://www.cms1924.org/WebPage/WebPage_75_110.aspx',
                  'http://www.cms1924.org/WebPage/WebPage_75_111.aspx',
                  'http://www.cms1924.org/WebPage/WebPage_75_398.aspx',
                  'http://www.cms1924.org/WebPage/WebPage2_75_87_112.aspx',
                  'http://www.cms1924.org/WebPage/WebPage2_75_88_114.aspx']

    # callback function
    def parsecontent_temps(self, response):
        # parameters can be got by response.meta['key']
        # url = response.meta['url']

        title = response.xpath('//td[@class ="contentTitle"]/text()')[0].extract()
        content_temp = response.xpath('//td[@class="contentDetail"]')[0].extract()

        if re.findall("<a target=\"_blank\" href=\"(\S*)\.pdf\"", content_temp):
            file_url = re.findall("<a target=\"_blank\" href=\"[^\"]*\"", content_temp)
            file_name = re.findall("<a target=\"_blank\" href=\"[^\"]*\">(\S*)</a>", content_temp)
            file_url[0] = re.sub("<a target=\"_blank\" href=\"", "", file_url[0])
            file_url[0] = re.sub("\"", "", file_url[0])
            name = file_name[0].split('/')
            if not os.path.exists('file/A-08/'):
                os.mkdir('file/A-08/')
            print('file/A-08/' + str(name[len(name) - 1]) + ' ' + "http://www.cms1924.org" + file_url[0])
            urllib.request.urlretrieve("http://www.cms1924.org" + file_url[0], 'file/A-08/' + str(name[len(name) - 1]))

        # use regular expression to resolve the pages you get, especially html elements
        content_temp = re.sub('<[^>]+>', '', content_temp)
        content_temp = re.sub('[\t\n\r]', '', content_temp)
        content_temp = re.sub(' +', ' ', content_temp)

        # open the file and write and close it
        csvfile = open('output/A-08.csv', 'a', newline='', errors='ignore', encoding='gbk')
        writer = csv.writer(csvfile)
        writer.writerow([title, content_temp])
        csvfile.flush()
        csvfile.close()

    def parse(self, response):
        # the rules how to deal with the pages you get
        # learn more about 'xpath' grammar
        conference = response.xpath('//span[@id]').re("<a href=\"([^\"]*)\"")

        # if the page you want is a secondary page and you can only get their urls, you can collect the urls and then use function Requset()
        urls = []

        for i in range(len(conference)):
            url = 'http://www.cms1924.org/WebPage/' + conference[i]  # conference[i].xpath('//a/@href').extract()[0]
            print(url)
            urls.append(url)
        for url in urls:
            # parameters can be passed by meta={'key':value}
            yield Request(url, meta={'url': url}, callback=self.parsecontent_temps)
            # urllib.request.urlretrieve(url, 'filePath/fileName.xxx')
