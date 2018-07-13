from scrapy.spiders import Spider
from scrapy.http import Request
import csv
import re
import urllib
import urllib.response
import os

class A10Spide(Spider):
    # name of the crawler(primary key)
    name = 'A-10'
    # urls which contain pages you want
    start_urls = ['http://www.geosociety.org.cn/?category=Z2VvZXhjaGFuZ2VOZXdz',
                  'http://www.geosociety.org.cn/?category=Z2VvZXhjaGFuZ2VOZXdz&page=2']

    # callback function
    def parsecontent_temps(self, response):
        # parameters can be got by response.meta['key']
        # url = response.meta['url']
        t = response.xpath('//td[@style="width:700px;text-align:center;font-size:24px;font-weight:bold;line-height:40px;color:#000000;"]/text()')[0].extract()

        # content_temp = response.xpath('//td[@style="FONT-SIZE: 16pt; FONT-FAMILY: 宋体; mso-ascii-font-family: \'Times New Roman\'; mso-hansi-font-family: \'Times New Roman\'"]')[0].extract()

        # t = response.xpath('//p[@class="MsoNormal"]/span').re('style="FONT-SIZE: 22pt; COLOR: red; FONT-FAMILY: 宋体; mso-ascii-font-family: \'Times New Roman\'; mso-hansi-font-family: \'Times New Roman\'">(\S*)</span>')
        c1 = response.xpath('//p[@align="left"]').extract()
        c2 = response.xpath('//p[@class ="MsoNormal"]').extract()
        c3 = response.xpath('//p[@style="width:730px;text-align:left;line-height:28px;"]').extract()

        # c2 = response.xpath('//p[@style="text-align:left;text-indent:2em;font-family:SimSun;font-size:18px;"]').re("\">(\S*)</p>")
        title = t
        content_temp = ''
        for i in c1:
            content_temp += i
        for i in c2:
            content_temp += i
        for i in c3:
            content_temp += i

        # if re.findall("<a target=\"_blank\" href=\"(\S*)\.pdf\"", content_temp):
        #     file_url = re.findall("<a target=\"_blank\" href=\"[^\"]*\"", content_temp)
        #     file_name = re.findall("<a target=\"_blank\" href=\"[^\"]*\">(\S*)</a>", content_temp)
        #     file_url[0] = re.sub("<a target=\"_blank\" href=\"", "", file_url[0])
        #     file_url[0] = re.sub("\"", "", file_url[0])
        #     name = file_name[0].split('/')
        #     if not os.path.exists('file/A-08/'):
        #         os.mkdir('file/A-08/')
        #     print('file/A-08/' + str(name[len(name) - 1]) + ' ' + "http://www.cms1924.org" + file_url[0])
        #     urllib.request.urlretrieve("http://www.cms1924.org" + file_url[0], 'file/A-08/' + str(name[len(name) - 1]))

        # use regular expression to resolve the pages you get, especially html elements
        content_temp = re.sub('<[^>]+>', '', content_temp)
        content_temp = re.sub('[\t\n\r]', '', content_temp)
        content_temp = re.sub(' +', ' ', content_temp)

        # open the file and write and close it
        csvfile = open('output/A-10.csv', 'a', newline='', errors='ignore', encoding='gbk')
        writer = csv.writer(csvfile)
        writer.writerow([title, content_temp])
        csvfile.flush()
        csvfile.close()

    def parse(self, response):
        # the rules how to deal with the pages you get
        # learn more about 'xpath' grammar
        conference = response.xpath('//td[@style="text-align:left;line-height:28px;border-bottom:1px #DBDBDB dashed;"]/a').re("<a href=\"([^\"]*)\"")

        # if the page you want is a secondary page and you can only get their urls, you can collect the urls and then use function Requset()
        urls = []

        for i in range(len(conference)):
            conference[i] = re.sub('amp;', '', conference[i])
            url = 'http://www.geosociety.org.cn/' + conference[i]  # conference[i].xpath('//a/@href').extract()[0]
            print(url)
            urls.append(url)
        for url in urls:
            # parameters can be passed by meta={'key':value}
            yield Request(url, meta={'url': url}, callback=self.parsecontent_temps)
            # urllib.request.urlretrieve(url, 'filePath/fileName.xxx')
