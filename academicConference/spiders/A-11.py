from scrapy.spiders import Spider
from scrapy.http import Request
import csv
import re
import urllib
import urllib.response
import os

class A11Spide(Spider):
    # name of the crawler(primary key)
    name = 'A-11'
    # urls which contain pages you want
    start_urls = ['http://www.gsc.org.cn/n1313394/n1330239/index_9.html',
                  'http://www.gsc.org.cn/n1313394/n1330239/index_8.html',
                  'http://www.gsc.org.cn/n1313394/n1330239/index_7.html',
                  'http://www.gsc.org.cn/n1313394/n1330239/index_6.html',
                  'http://www.gsc.org.cn/n1313394/n1330239/index_5.html',
                  'http://www.gsc.org.cn/n1313394/n1330239/index_4.html',
                  'http://www.gsc.org.cn/n1313394/n1330239/index_3.html']

    # callback function
    def parsecontent_temps(self, response):
        # parameters can be got by response.meta['key']
        # url = response.meta['url']
        t = response.xpath('//div[@id="cke_pastebin"]/p[1]').extract()
        if not t:
            t = response.xpath('//td[@class="STYLE3"]/p[1]').extract()

        # content_temp = response.xpath('//td[@style="FONT-SIZE: 16pt; FONT-FAMILY: 宋体; mso-ascii-font-family: \'Times New Roman\'; mso-hansi-font-family: \'Times New Roman\'"]')[0].extract()

        # t = response.xpath('//p[@class="MsoNormal"]/span').re('style="FONT-SIZE: 22pt; COLOR: red; FONT-FAMILY: 宋体; mso-ascii-font-family: \'Times New Roman\'; mso-hansi-font-family: \'Times New Roman\'">(\S*)</span>')
        c = response.xpath('//div[@id="cke_pastebin"]/p[position()>1]').extract()
        if not c:
            c = response.xpath('//td[@class="STYLE3"]/p[position()>1]').extract()

        title = ''
        for i in t:
            title += i

        title = re.sub('<[^>]+>', '', title)
        title = re.sub('[\t\n\r]', '', title)
        title = re.sub(' +', ' ', title)

        content_temp = ''
        for i in c:
            content_temp += i

        # use regular expression to resolve the pages you get, especially html elements
        content_temp = re.sub('<[^>]+>', '', content_temp)
        content_temp = re.sub('[\t\n\r]', '', content_temp)
        content_temp = re.sub(' +', ' ', content_temp)

        # open the file and write and close it
        csvfile = open('output/A-11.csv', 'a', newline='', errors='ignore', encoding='gbk')
        writer = csv.writer(csvfile)
        if title == '':
            title = response.url
        writer.writerow([title, content_temp])
        csvfile.flush()
        csvfile.close()

        relative_urls = response.xpath('..//a[@href]').re("<a href=\"([^\"]*)\"")
        if relative_urls:
            for i in range(len(relative_urls)):
                relative_url = relative_urls[i]
                relative_url = re.sub('<[^>]+>', '', relative_url)
                relative_url = re.sub('[\t\n\r]', '', relative_url)
                relative_url = re.sub(' +', ' ', relative_url)
                absolute_url = 'http://www.gsc.org.cn/' + relative_url
                if re.findall("(\S*)\.pdf|(\S*)\.doc", absolute_url):
                    name = absolute_url.split('/')
                    if not os.path.exists('file/A-11/'):
                        os.mkdir('file/A-11/')
                    print('file/A-11/' + str(name[len(name) - 1]) + ' ' + absolute_url)
                    urllib.request.urlretrieve(absolute_url, 'file/A-11/' + str(name[len(name) - 1]))

    def parse(self, response):
        # the rules how to deal with the pages you get
        # learn more about 'xpath' grammar
        conference = response.xpath('//td[@height="24"]/a').re("<a href=\"([^\"]*)\"")

        # if the page you want is a secondary page and you can only get their urls, you can collect the urls and then use function Requset()
        urls = []

        for i in range(len(conference)):
            url = 'http://www.gsc.org.cn' + conference[i]  # conference[i].xpath('//a/@href').extract()[0]
            print(url)
            urls.append(url)
        for url in urls:
            # parameters can be passed by meta={'key':value}
            yield Request(url, meta={'url': url}, callback=self.parsecontent_temps)
            # urllib.request.urlretrieve(url, 'filePath/fileName.xxx')
