from scrapy.spiders import Spider
import csv


class A01Spide(Spider):
    # name of the crawler(primary key)
    name = 'A-01'
    # urls which contain pages you want
    start_urls = ['http://www.cms.org.cn/discusspub/0_0_0_0.html',
                  'http://www.cms.org.cn/discusspub/1_1_0_0.html',
                  'http://www.cms.org.cn/discusspub/1_2_0_0.html',
                  'http://www.cms.org.cn/discusspub/1_22_0_0.html',
                  'http://www.cms.org.cn/discusspub/1_23_0_0.html',
                  'http://www.cms.org.cn/discusspub/1_24_0_0.html',
                  'http://www.cms.org.cn/discusspub/1_25_0_0.html',
                  'http://www.cms.org.cn/discusspub/1_26_0_0.html',
                  'http://www.cms.org.cn/discusspub/1_27_0_0.html',
                  'http://www.cms.org.cn/discusspub/1_28_0_0.html',
                  'http://www.cms.org.cn/discusspub/1_29_0_0.html',
                  'http://www.cms.org.cn/discusspub/1_30_0_0.html',
                  'http://www.cms.org.cn/discusspub/1_31_0_0.html',
                  'http://www.cms.org.cn/discusspub/1_32_0_0.html',
                  'http://www.cms.org.cn/discusspub/1_33_0_0.html',
                  'http://www.cms.org.cn/discusspub/1_34_0_0.html',
                  'http://www.cms.org.cn/discusspub/1_35_0_0.html',
                  'http://www.cms.org.cn/discusspub/1_36_0_0.html',
                  'http://www.cms.org.cn/discusspub/1_65_0_0.html',
                  'http://www.cms.org.cn/discusspub/1_66_0_0.html',
                  'http://www.cms.org.cn/discusspub/1_67_0_0.html',
                  'http://www.cms.org.cn/discusspub/1_69_0_0.html',
                  'http://www.cms.org.cn/discusspub/1_70_0_0.html'
                  ]

    def parse(self, response):
        # the rules how to deal with the pages you get
        # learn more about 'xpath' grammar
        conference = response.xpath('//div[@class="discuss2Page"]//div[@class="dec"]')

        # open file and write
        csvfile = open('output/A-01.csv', 'a', newline='', errors='ignore', encoding='gbk')
        writer = csv.writer(csvfile)

        for i in range(len(conference)):
            title = conference[i].xpath('.//div[@class="title"]/p/text()')[0].extract()
            info_value = conference[i].xpath('.//div[@class="info"]/p/text()')
            info_name = conference[i].xpath('.//div[@class="info"]/p/strong/text()')
            content = ''
            for j in range(len(info_value)):
                content += info_name[j].extract() + info_value[j].extract() + ' '
            # write to file
            writer.writerow([title, content])

        # close the file
        csvfile.flush()
        csvfile.close()

