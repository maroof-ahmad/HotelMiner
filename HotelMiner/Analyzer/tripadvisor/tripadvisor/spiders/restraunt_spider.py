import scrapy
import unicodedata

#call this spider like
#scrapy crawl tripadvisorspider -o output.json -a url=www.something.com

def unicode_to_string(u):
    return unicodedata.normalize('NFKD', u).encode('ascii','ignore').strip()


class TripAdvisorSpider(scrapy.Spider):
    name='tripadvisorspider'
    allowed_domains=['www.tripadvisor.in']
    start_urls=[]
    base_uri = 'https://www.tripadvisor.in'

    #appending url to start_urls in constructor
    def __init__(self, url=None, *args, **kwargs):
        super(TripAdvisorSpider, self).__init__(*args, **kwargs)
        self.start_urls.append(url)


    def parse_review(self,review):

        #quote
        u_quote = review.css('.quote::text').extract()[0]
        quote = unicode_to_string(u_quote)

        #stars
        u_stars = review.css('.sprite-rating_s_fill::attr(alt)').extract()[0]
        stars = unicode_to_string(u_stars)[0]
        try:
            u_reviewDate = review.css('.ratingDate::attr(title)').extract()[0]
        except:
            u_reviewDate = review.css('.ratingDate::text').extract()[0]
            u_reviewDate = u_reviewDate[9:]
        reviewDate = unicode_to_string(u_reviewDate)

        #reviewBody
        u_reviewBody = ''.join((review.css('.entry')[0]).xpath("p//text()").extract()).strip()
        reviewBody = unicode_to_string(u_reviewBody)

        yield {
        'reviewTitle':quote,
        'totalRating':stars,
        'reviewContent':reviewBody,
        'reviewDate':u_reviewDate
        }

    def start_requests(self):
        for link in self.start_urls:
            yield scrapy.Request(link,callback = self.parse,errback = self.err_handler)


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
    def parse(self, response):
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
            yield scrapy.Request(next_page_uri,callback = self.parse,errback = self.err_handler)
