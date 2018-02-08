# coding:utf-8
import time
import scrapy
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from price.items import PriceItem
from selenium import webdriver  # 自动化监测工具
from selenium.webdriver.common.action_chains import ActionChains

class Price(CrawlSpider):
    name = "price"
    host = 'https://www.haoinvest.com'
    start_urls = ['https://www.haoinvest.com/Invest/hot/p/1.html']
    num = 1

    def parse(self, response):
        selector = Selector(response)
        lis = selector.xpath('//*[@id="picList"]/li')
        for li in lis:
            url = self.host + li.xpath('div[6]/a/@href').extract_first()

            # chrome driver location
            driverlocation = '/usr/local/software/chromeDriver/chromedriver'

            # use
            driver = webdriver.Chrome(driverlocation)

            # 打开网页
            driver.get(url)

            # 鼠标偏移到指定位置
            above = driver.find_element_by_css_selector(".tabs_list:nth-child(3)")
            ActionChains(driver).move_to_element(above).perform()

            # 暂停3秒
            time.sleep(3)

            items = driver.find_element_by_css_selector('.invest_list').text.split("\n")
            del items[0]
            for item in items:
                yield self.parseItem(item)

        nextstr = selector.css('#Pagination div .next::attr(href)').extract_first()
        self.num = self.num + 1
        if nextstr and self.num < 101:
            nextpage = self.host + nextstr
            yield scrapy.Request(nextpage, callback=self.parse)

    def parseItem(self, value):
        item = PriceItem()
        temp = value.split(" ")
        item['people'] = temp[0]
        item['price'] = temp[1]
        item['ctime'] = temp[2] + ' ' + temp[3]

        return item




