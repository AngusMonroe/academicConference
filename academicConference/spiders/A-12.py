from scrapy.spiders import Spider
from scrapy.http import Request
import csv
import re
import urllib
import urllib.response
import os

class A12Spide(Spider):
    # name of the crawler(primary key)
    name = 'A-12'
    # urls which contain pages you want
    start_urls = ['http://www.cgscgs.org.cn/drupal/?q=node/613',
                  'http://www.cgscgs.org.cn/drupal/?q=node/711',
                  'http://www.cgscgs.org.cn/drupal/?q=node/479',
                  'http://www.cgscgs.org.cn/drupal/?q=node/394',
                  'http://www.cgscgs.org.cn/drupal/?q=node/372',
                  'http://www.cgscgs.org.cn/drupal/?q=node/2',
                  'http://www.cgscgs.org.cn/drupal/?q=node/171',
                  'http://www.cgscgs.org.cn/drupal/?q=node/157',
                  'http://www.cgscgs.org.cn/drupal/?q=node/158',
                  'http://www.cgscgs.org.cn/drupal/?q=node/160',
                  'http://www.cgscgs.org.cn/drupal/?q=node/159',
                  'http://www.cgscgs.org.cn/drupal/?q=node/161',
                  'http://www.cgscgs.org.cn/drupal/?q=node/162',
                  'http://www.cgscgs.org.cn/drupal/?q=node/163',
                  'http://www.cgscgs.org.cn/drupal/?q=node/164']

    # callback function
    def parsecontent_temps(self, response):
        print("This is a html.")

    def parse(self, response):
        # the rules how to deal with the pages you get
        # learn more about 'xpath' grammar
        conference = response.xpath('//td/a[1]').re("<a href=\"([^\"]*)\"")
        t = response.xpath('//a[1]/font[@style="line-height:130%;"]/text()').extract()

        csvfile = open('output/A-12.csv', 'a', newline='', errors='ignore', encoding='gbk')
        writer = csv.writer(csvfile)

        for i in range(len(conference)):
            print(conference[i])
            if re.findall("(\S*)\.pdf", conference[i]) or re.findall("(\S*)\.doc", conference[i]):
                name = conference[i].split('/')
                if not os.path.exists('file/A-12/'):
                    os.mkdir('file/A-12/')
                print('file/A-12/' + str(name[len(name) - 1]) + ' ' + conference[i])
                try:
                    urllib.request.urlretrieve(conference[i], 'file/A-12/' + str(name[len(name) - 1]))
                    writer.writerow([t[i], conference[i]])
                except Exception:
                    writer.writerow([t[i], ''])
                    print("Error!")
                    continue

            else:
                print("This is a html.")
                # yield Request(conference[i], meta={'url': conference[i]}, callback=self.parsecontent_temps)

        # close the file
        csvfile.flush()
        csvfile.close()