# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MalScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    title = scrapy.Field()
    poster_img_url = scrapy.Field()
    mal_url = scrapy.Field()
    mal_id = scrapy.Field()
    synonym_name = scrapy.Field()
    japanese_name = scrapy.Field()
    english_name = scrapy.Field()
    show_type = scrapy.Field()
    episodes = scrapy.Field()
    status = scrapy.Field()
    airing_start_date = scrapy.Field()
    airing_finish_date = scrapy.Field()
    premiered = scrapy.Field()
    broadcast = scrapy.Field()
    producers = scrapy.Field()
    licensors = scrapy.Field()
    studios = scrapy.Field()
    source = scrapy.Field()
    genres = scrapy.Field()
    themes = scrapy.Field()
    demographic = scrapy.Field()
    duration_in_minutes = scrapy.Field()
    age_rating = scrapy.Field()
    score = scrapy.Field()
    members = scrapy.Field()
    official_site = scrapy.Field()
    anidb_url = scrapy.Field()
    ann_url = scrapy.Field()
    wikipedia_url = scrapy.Field()
    description = scrapy.Field()
