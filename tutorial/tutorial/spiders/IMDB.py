import scrapy
import datetime
from datetime import datetime, timedelta
import re
import dateutil
from dateutil import parser


class MoviesSpider(scrapy.Spider):
    name = 'imdb_movies'

    custom_settings = {
        "DOWNLOAD_DELAY": 5,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    }

    start_urls = [
        "http://www.imdb.com/search/title?title_type=feature&release_date=1998-01-1,1998-12-31&genres=drama&languages=en"
    ]

    def parse(self, response):
        # Extract the links to the individual festival pages
        movies_link = response.xpath('//h3[@class="lister-item-header"]/a/@href').extract()
        movies_names = response.xpath('//h3[@class="lister-item-header"]/a/text()').extract()
        
        for i in range(len(movies_link)):
            
            yield scrapy.Request(
                url="http://www.imdb.com"+movies_link[i],
                callback=self.parse_movies, 
                meta={'url': movies_link[i], 'name': movies_names[i]}
            )

            next_url = response.xpath('//a[@class="lister-page-next next-page"]/@href').extract()



        yield scrapy.Request(
            url=next_url,
            callback=self.parse
        )

    def parse_movies(self, response):
        
        name = response.request.meta['name']
        
        url = response.request.meta['url']

        imdb_score = float(response.xpath("//span[@itemprop='ratingValue']/text()").extract()[0])

        budget = int("".join(response.xpath('//h4[contains(text(), "Budget:")]/following-sibling::node()/descendant-or-self::text()').extract()[0].strip().split(","))[1:])

        gross_income = int("".join(response.xpath('//h4[contains(text(), "Gross USA:")]/following-sibling::node()/descendant-or-self::text()').extract()[0].strip().split(","))[1:])

        language = response.xpath('//div[@id="titleDetails"]/div/a[contains(@href, "language")]/text()').extract()[0].strip()

        num_voted_users = response.xpath('//span[@itemprop="ratingCount"]/text()').extract()[0].strip()

        director_name = response.xpath('//span[@itemprop="director"]/a/span/text()').extract()[0]

        duration = (response.xpath('//time[@itemprop="duration"]/text()').extract()[0].strip())

        duration_sorted = int(duration[0])*60+int(duration[3:5])

        cast_list = response.xpath('//table[@class="cast_list"]//td[@class="itemprop"]/a/span[@class="itemprop"]/text()').extract()

        awards = response.xpath('//span[@class = "see-more inline"]/a/@href').extract()[0]

        worldwide_income = int("".join(response.xpath('//h4[contains(text(), "Cumulative Worldwide Gross:")]/following-sibling::node()/descendant-or-self::text()').extract()[0].strip().split(","))[1:])

        genres = response.xpath('//h4[contains(text(), "Genres:")]/following-sibling::node()/descendant-or-self::text()').extract() 

        genres_cleaned = [elem.strip(',| \n ""') for elem in genres]  
            
        release_date = response.xpath('//h4[contains(text(), "Release Date:")]/following-sibling::node()/descendant-or-self::text()').extract()[0].strip() 


        yield {
            'url': url,
            'name': name,
            'budget': budget,
            'gross_income': gross_income,
            'imdb_score': imdb_score,
            'num_voted_users': num_voted_users,
            'director_name': director_name,
            'duration_sorted': duration_sorted,
            'cast_list': cast_list,
            'awards': awards,
            'worldwide_income': worldwide_income,
            'genres cleaned': genres_cleaned,
            'release_date': release_date

            }



#<a href="?title_type=feature&amp;release_date=2000-01-01,2016-12-31&amp;genres=drama&amp;languages=en&amp;page=2&amp;ref_=adv_nxt" class="lister-page-next next-page" ref-marker="adv_nxt">Next »</a>
#response.xpath('//span[@class = "see-more inline"]/a/@href').extract()[0]
        