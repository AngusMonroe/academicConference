from scrapy.spiders import Spider
import csv
import re


class A03Spide(Spider):
    # name of the crawler(primary key)
    name = 'A-03'
    # urls which contain pages you want
    start_urls = ['http://www.cstam.org.cn/channel/103.html#boxs']
    for i in range(2, 51):
        start_urls.append('http://www.cstam.org.cn/channel/103/' + str(i) + '.html#boxs')

    def parse(self, response):
        # the rules how to deal with the pages you get
        # learn more about 'xpath' grammar
        conference = response.xpath('//div[@class="lb_right_list"]/ul/li/a').re("title=\"([^\"]*)\"")
        url = response.xpath('//div[@class="lb_right_list"]/ul/li/a').re("href=\"([^\"]*)\"")

        # open file and write
        csvfile = open('output/A-03.csv', 'a', newline='', errors='ignore', encoding='gbk')
        writer = csv.writer(csvfile)


        for i in range(len(conference)):
            writer.writerow([conference[i], 'http://www.cstam.org.cn' + url[i]])

        # close the file
        csvfile.flush()
        csvfile.close()

