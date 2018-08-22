from scrapy.spiders import Spider
from scrapy.http import Request
import csv
import re
import urllib

class D22Spide(Spider):
    # name of the crawler(primary key)
    name = 'D-22'
    # urls which contain pages you want
    start_urls = ['http://www.fyxh.org/plus/list.php?tid=8',
                  'http://www.fyxh.org/plus/list.php?tid=8&TotalResult=45&PageNo=2',
                  'http://www.fyxh.org/plus/list.php?tid=8&TotalResult=45&PageNo=3',
                  'http://www.fyxh.org/plus/list.php?tid=8&TotalResult=45&PageNo=4',
                  'http://www.fyxh.org/plus/list.php?tid=8&TotalResult=45&PageNo=5']

    # callback function
    def parseDetails(self, response):
        # parameters can be got by response.meta['key']
        # url = response.meta['url']

        title = response.xpath('//div[@align="center"]/span/text()')[0].extract()
        content_temp = response.xpath('//td[@style="padding:8px 10px 0px 10px; line-height:28px;"]')[0].extract()

        # use regular expression to resolve the pages you get, especially html elements
        content_temp = re.sub('<[^>]+>[^<]*</[^>]+>', '', content_temp)
        pattern_h5 = re.compile(r'<[^>]+>', re.S)
        pattern_blackLines = re.compile(r'\n{2,}', re.S)
        content = pattern_blackLines.sub('', pattern_h5.sub('', content_temp))
        content = re.sub('[\t\n\r]', '', content)
        content = re.sub('&nbsp;', '', content)
        content = re.sub(' +', ' ', content)

        # open the file and write and close it
        csvfile = open('output/D-22.csv', 'a', newline='', errors='ignore', encoding='gbk')
        writer = csv.writer(csvfile)
        writer.writerow([title, content])
        csvfile.flush()
        csvfile.close()

    def parse(self, response):
        # the rules how to deal with the pages you get
        # learn more about 'xpath' grammar
        conference = response.xpath('//table[@style="border-bottom:1px #D8D8D8 dotted;"]')

        # if the page you want is a secondary page and you can only get their urls, you can collect the urls and then use function Requset()
        urls = []

        for i in range(len(conference)):
            url = 'http://www.fyxh.org' + conference[i].xpath('.//a/@href').extract()[0]
            urls.append(url)

        # print(urls)

        for url in urls:
            # parameters can be passed by meta={'key':value}
            yield Request(url, meta={'url': url}, callback=self.parseDetails)
            # urllib.request.urlretrieve(url, 'filePath/fileName.xxx')