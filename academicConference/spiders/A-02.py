from scrapy.spiders import Spider
import re
import csv


class A02Spide(Spider):
    # name of the crawler(primary key)
    name = 'A-02'
    # urls which contain pages you want
    start_urls = ['http://www.cps-net.org.cn/academic/program.htm']

    def parse(self, response):
        # the rules how to deal with the pages you get
        # learn more about 'xpath' grammar
        title = response.xpath('//td[@valign="top"]').re("class=\"name_program\">([\S\s]*)</span>")
        detail = response.xpath('//td[@valign="top"]').re("</span>([\S\s]*)</td>")

        # open file and write
        csvfile = open('output/A-02.csv', 'a', newline='', errors='ignore', encoding='gbk')
        writer = csv.writer(csvfile)

        for i in range(max(len(title), len(detail))):
            t = ''
            if title[i]:
                title[i] = re.sub('<[^>]+>', '', title[i])
                t = title[i]

            d = ''
            if detail[i]:
                detail[i] = re.sub('<[^>]+>', '', detail[i])
                detail[i] = re.sub('[\t\n\r]', '', detail[i])
                detail[i] = re.sub(' +', ' ', detail[i])
                d = detail[i]

            # write to file
            writer.writerow([t, d])

        # close the file
        csvfile.flush()
        csvfile.close()
