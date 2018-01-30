import scrapy
import datetime
from datetime import datetime, timedelta
import re
import dateutil
from dateutil import parser


class MoviesSpider(scrapy.Spider):
    name = 'best_actress_movies'

    custom_settings = {
        "DOWNLOAD_DELAY": 5,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    }

    start_urls = [
        "https://en.wikipedia.org/wiki/Academy_Award_for_Best_Actress"
    ]

    def parse(self, response):
        # Extract the links to the individual festival pages
        year = response.xpath('//th[@scope = "row"]/a/text()').extract()
        actress_names = response.xpath('//span[@class="sorttext"]/a/text()').extract()

        for i in range(len(actress_names)):
            
            yield scrapy.Request( 
                callback = self.parse_actors,
                url = "https://en.wikipedia.org/wiki/Academy_Award_for_Best_Actress",
                meta = {'year': year, 'actress':actress_names})

            next_url = "https://en.wikipedia.org/wiki/Academy_Award_for_Best_Actress"
    
        yield scrapy.Request(
            url=next_url,
            callback=self.parse
        )

    def parse_actors(self, response):
              
        actress_names = response.request.meta['actress']
        
        year = response.request.meta['year']

        yield {

            'year' : year,
            'Actress': actress_names}


                