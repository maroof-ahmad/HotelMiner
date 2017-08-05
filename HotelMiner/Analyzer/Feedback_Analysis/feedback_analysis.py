#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name : Feedback Analysis Handler
#-------------------------------------------------------------------------------
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from tripadvisor.spiders.restraunt_spider import TripAdvisorSpider
from pprint import pprint
import json
from google_text_extraction import worker2
from adj_noun import worker3
from twisted.internet import reactor

# function to get the reviews from the scraper

def download_reviews(url):
    # with open('last_review.txt') as file:
    #     last_review = file.read()
    #     file.close()
    # process = CrawlerRunner(get_project_settings())
    process = CrawlerProcess(get_project_settings())
    # d = process.crawl(TripAdvisorSpider,url=url,last_review = 0)
    process.crawl(TripAdvisorSpider,url=url,last_review = 0)
    process.start()
    # d.addBoth(lambda _: reactor.stop())
    # reactor.run()


def worker(url):
    download_reviews(url)
    with open('reviews.txt') as data_file:

        # new_reviews = json.load(data_file)
        new_reviews = data_file.read()
    pprint(new_reviews)

    if len(new_reviews) == 0:
        print "no new reviews on the website"
        sys.exit()
    else:
        # save_reviews_to_db(new_reviews)
        # sentiment_analysis_result = sentiment_analysis(new_reviews)
        print "Worker 2 called"
        worker2()
        print "Worker 3 called"
        worker3()
        print "############################### The End ################################"

        with open('ans.json') as file:
            ans = json.load(file)
        ans = ans[0]
        results = dict()

        for key, value in ans.iteritems():
            a = set()
            for val in value:
                a.add(val)
            if len(value) != 0:
                results[key]=a

    return results
        # save_sentiment_to_db(sentiment_analysis_result)
