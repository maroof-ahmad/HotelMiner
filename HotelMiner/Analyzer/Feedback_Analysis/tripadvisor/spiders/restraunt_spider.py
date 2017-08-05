import os
import scrapy
import json
import unicodedata
from ..items import TripadvisorItem
from scrapy.exceptions import CloseSpider
from scrapy import signals
from scrapy import Spider

def unicode_to_string(u):
    return unicodedata.normalize('NFKD', u).encode('ascii','ignore').strip()



class TripAdvisorSpider(scrapy.Spider):
    name='tripadvisorspider'
    allowed_domains=['www.tripadvisor.in']
    start_urls=[]
    base_uri = 'https://www.tripadvisor.in'
    r_urls=[]
    r_urls_2=[]
    items = []
    custom_settings = {
        'CONCURRENT_REQUESTS':'1',
        'CONCURRENT_REQUESTS_PER_DOMAIN':'1',
    }

    #appending url to start_urls in constructor
    def __init__(self, *args, **kwargs):
        self.start_urls.append(kwargs.get('url'))
        # self.last_review = kwargs.get('last_review')


    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(TripAdvisorSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider


    def spider_closed(self, spider):
        # lr = self.r_urls[0].split('-')[3][1:]
        # print "yo",self.last_review
        # print "yo2",lr
        print "yo"
        # fpath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'last_review.txt')
        # print "fpath",fpath
        # with open(fpath,'w') as file:
        #     file.write(lr + '\n')
        #     file.close()
        with open('reviews.txt', 'w') as f:
            big_one = ""
            for item in self.items:
                big_one = big_one + ". " + item["reviewBody"]
            # big_one_vec = []
            # big_one_vec.append(big_one)
            # json.dump(big_one_vec,f,indent=4,separators=(',', ':'))
            f.write(big_one)
            f.close()
        return


    def parse_review(self,review):
        # print "Parse Review Called"
        item = TripadvisorItem()

        #review_id
        u_review_id = review.css('.reviewSelector::attr(id)')[0].extract().split('_')[1]
        review_id = unicode_to_string(u_review_id)
        item['_id'] = review_id

        #quote
        u_quote = review.css('.quote::text').extract()[0]
        quote = unicode_to_string(u_quote)
        item['quote'] = quote

        #stars
        u_stars = review.css('.sprite-rating_s_fill::attr(alt)').extract()[0]
        stars = unicode_to_string(u_stars)[0]
        item['stars'] = stars

        #reviewDate
        try:
            u_reviewDate = review.css('.ratingDate::attr(title)').extract()[0]
        except:
            u_reviewDate = review.css('.ratingDate::text').extract()[0]
            u_reviewDate = u_reviewDate[9:]
        reviewDate = unicode_to_string(u_reviewDate)
        item['reviewDate'] = reviewDate

        #reviewBody
        u_reviewBody = ''.join((review.css('.entry')[0]).xpath("p//text()").extract()).strip()
        reviewBody = unicode_to_string(u_reviewBody)
        item['reviewBody'] = reviewBody

        self.items.append(dict(item))
        # print dict(item)



    def start_requests(self):
        for link in self.start_urls:
            yield scrapy.Request(link,callback = self.parse_links,errback = self.err_handler)


    #Error Handler Method
    def err_handler(self,failure):
        # log all error failures
        self.logger.error(repr(failure))

        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        #DNS Lookup Error
        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        #TImeout Error
        elif failure.check(TimeoutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)

    #Page Parser
    # def parse_links(self, response):
    #     reviewList = response.css('.reviewSelector')
    #     for review in reviewList:
    #         u_href = review.css('.quote a::attr(href)').extract()[0]
    #         href = unicode_to_string(u_href)
    #         review_uri = self.base_uri+href
    #         self.r_urls.append(review_uri)
    #
    #     next_page_selector = response.css('.unified.pagination').xpath("//a[text()[contains(.,'Next')]]")
    #     next_page = next_page_selector.extract_first()
    #
    #     if next_page is not None:
    #         u_href = next_page_selector.css("a::attr(href)").extract_first()
    #         href = unicode_to_string(u_href)
    #         next_page_uri = self.base_uri + href
    #         #request for parsing the next page
    #         yield scrapy.Request(next_page_uri,callback = self.parse_links,errback = self.err_handler)
    #     else:
    #         # print "else called"
    #         if self.last_review == "" :
    #             self.r_urls_2 = self.r_urls
    #         else:
    #             for rurl in self.r_urls:
    #                 # print "rurl ",rurl
    #                 rid = rurl.split('-')[3][1:]
    #                 # print "rid",rid
    #                 if rid == self.last_review:
    #                     idx = self.r_urls.index(rurl)
    #                     self.r_urls_2 = self.r_urls[0:idx]
    #                     # raise CloseSpider('got what was needed')
    #         for rurl in self.r_urls_2:
    #             yield scrapy.Request(rurl,callback=self.parse_review,errback = self.err_handler)
            # self.process_urls()


    def parse_links(self, response):
        reviewList = response.css('.reviewSelector')
        for review in reviewList:
            u_href = review.css('.quote a::attr(href)').extract()[0]
            href = unicode_to_string(u_href)
            review_uri = self.base_uri+href
            #request for page of individual review
            yield scrapy.Request(review_uri,callback=self.parse_review,errback = self.err_handler)
        next_page_selector = response.css('.unified.pagination').xpath("//a[text()[contains(.,'Next')]]")
        next_page = next_page_selector.extract_first()
        #if next page exists
        if next_page is not None:
            u_href = next_page_selector.css("a::attr(href)").extract_first()
            href = unicode_to_string(u_href)
            next_page_uri = self.base_uri + href
            #request for parsing the next page
            yield scrapy.Request(next_page_uri,callback = self.parse_links,errback = self.err_handler)
