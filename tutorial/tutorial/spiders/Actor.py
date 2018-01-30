import scrapy
import datetime
from datetime import datetime, timedelta
import re
import dateutil
from dateutil import parser


class MoviesSpider(scrapy.Spider):
    name = 'best_actor_movies'

    custom_settings = {
        "DOWNLOAD_DELAY": 5,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    }

    start_urls = [
        "https://en.wikipedia.org/wiki/Academy_Award_for_Best_Actor"
    ]

    def parse(self, response):
        # Extract the links to the individual festival pages
        year = response.xpath('//th[@scope = "row"]/a/text()').extract()
        actor_names = response.xpath('//span[@class="sorttext"]/a/text()').extract()

        for i in range(len(actor_names)):
            
            yield scrapy.Request( 
                callback = self.parse_actors,
                url = "https://en.wikipedia.org/wiki/Academy_Award_for_Best_Actor",
                meta = {'year': year[i], 'actor':actor_names[i]})

            next_url = "https://en.wikipedia.org/wiki/Academy_Award_for_Best_Actor"
    
        yield scrapy.Request(
            url=next_url,
            callback=self.parse
        )

    def parse_actors(self, response):
              
        actor_names = response.request.meta['actor']
        
        year = response.request.meta['year']

        yield {

            'year' : year,
            'Actor': actor_names}

                