import scrapy
from mal_scraper.items import MalScraperItem


class MalSpiderSpider(scrapy.Spider):
    name = "mal_spider"
    allowed_domains = ["myanimelist.net"]
    start_urls = ["https://myanimelist.net/anime/season/archive"]

    def parse(self, response):
        season_url_items = response.css('tr a')

        for season_url_item in [season_url_items[0]]:
            season_url = season_url_item.attrib['href']
            season_year = season_url_item.css('::text').get()

            # yield scrapy.Request(
            #     url=season_url,
            #     callback=self.seasonal_anime_page,
            #     meta={'playwright': True})
            yield response.follow(
                url=season_url,
                callback=self.seasonal_anime_page
                )


    def seasonal_anime_page(self, response):
        seasonal_shows_lists = response.css("div.js-seasonal-anime-list")

        seasonal_show_urls = []
        for seasonal_shows_list in seasonal_shows_lists:
            anime_header = seasonal_shows_list.css("div.anime-header::text").get()
            if anime_header != "TV (Continuing)":
                 [seasonal_show_urls.append(seasonal_title) for seasonal_title in  seasonal_shows_list.css("h2.h2_anime_title a")]

        for titles in seasonal_show_urls:
            seasonal_shows_url = titles.attrib["href"]
            yield response.follow(url=seasonal_shows_url, callback=self.anime_page)


    def anime_page(self, response):
        # In this function wee want title, id from url, type, episodes,
        # status, aired, premiered, producers, Licensors
        # studios, source, genre, theme, demographic, duration, rating
        # score & rated by user number, ranked, members, favorites,
        # official site, resources
        # streaming platform, synopsis, prequal/sequal/alternative with id
        mal_item = MalScraperItem()
        title = response.css('div.h1-title h1.title-name strong::text').get()
        poster_img_url = response.xpath('//img[@itemprop="image"]').attrib['data-src']
        mal_url = response.url
        mal_id = response.url.split("/")[4]
        sidebar_information = response.css('div.spaceit_pad')

        # alternative_names
        synonym_name = None
        japanese_name = None
        english_name = None
        show_type = None
        episodes = None
        status = None
        airing_start_date = None
        airing_finish_date = None
        premiered = None
        broadcast = None
        producers = None
        licensors = None
        studios = None
        source = None
        genres = None
        themes = None
        demographic = None
        duration_in_minutes = None
        age_rating = None
        score = None
        members = None
        official_site = None
        anidb_url = None
        ann_url = None
        wikipedia_url = None

        description = response.xpath("//p[@itemprop='description']/node()").getall()
        description = "".join(description)

        for name in sidebar_information[:3]:
            language = name.css('span.dark_text::text').get().strip()
            alternative_title = name.css("::text")[2].get()
            if language == "Japanese:":
                japanese_name = alternative_title
            elif language == "English:":
                english_name = alternative_title
            elif language == "Synonyms:":
                synonym_name = alternative_title

        for info in sidebar_information:
            info_key_text = info.css('span.dark_text::text').get()
            info_value_text = info.css("::text")

            if info_key_text == "Type:":
                show_type = info_value_text[3].get()
            elif info_key_text == "Episodes:":
                episodes = info_value_text[2].get()
            elif info_key_text == "Status:":
                status = info_value_text[2].get()
            elif info_key_text == "Aired:":
                aired = info_value_text[2].get()
                aired = aired.split(" to ")
                airing_start_date = aired[0]
                if len(aired) > 1:
                    airing_finish_date = aired[1]
                    if "?" in airing_finish_date:
                        airing_finish_date = None
                else:
                    airing_finish_date = None
            elif info_key_text == "Premiered:":
                premiered = info_value_text[3].get()
            elif info_key_text == "Broadcast:":
                broadcast = info_value_text[2].get()
            elif info_key_text == "Producers:":
                if "None found" not in info_value_text[2].get():
                    producers = "".join([i.get() for i in info_value_text[3:]])
            elif info_key_text == "Licensors:":
                if "None found" not in info_value_text[2].get():
                    licensors = "".join([i.get() for i in info_value_text[3:]])
            elif info_key_text == "Studios:":
                if "None found" not in info_value_text[2].get():
                    studios = "".join([i.get() for i in info_value_text[3:]])
            elif info_key_text == "Source:":
                source = "".join([i.get() for i in info_value_text[2:]])
            elif info_key_text == "Genres:" or info_key_text == "Genre:":
                genres = ", ".join([i.get() for i in info.css("a::text")])
            elif info_key_text == "Themes:" or info_key_text == "Theme:":
                themes = ", ".join([i.get() for i in info.css("a::text")])
            elif info_key_text == "Demographic:":
                demographic = info_value_text[3].get()
            elif info_key_text == "Duration:":
                duration_in_minutes = info_value_text[2].get()
            elif info_key_text == "Rating:":
                age_rating = info_value_text[2].get()
                if "None" in age_rating:
                    age_rating = None
            elif info_key_text == "Score:":
                score = info_value_text[3].get()
            elif info_key_text == "Members:":
                members = info_value_text[2].get()

            # get external resources links
            external_links_list = response.css("div.external_links a")
            for link in external_links_list:
                link_text = link.css("::text").get()
                url = link.attrib['href']
                if link_text == "Official Site":
                    official_site = url
                elif link_text == "AniDB":
                    anidb_url = url
                elif link_text == "ANN":
                    ann_url = url
                elif link_text == "Wikipedia":
                    if "en.wikipedia.org" in url:
                        wikipedia_url = url

        related_media_table = response.css("table.anime_detail_related_anime tr")
        sequal_mal_id_name = None
        for row in related_media_table:
            if row.css("td.ar::text").get() == "Sequel:":
                mal_id = row

        mal_item["title"] = title
        mal_item["poster_img_url"] = poster_img_url
        mal_item["mal_url"] = mal_url
        mal_item["mal_id"] = mal_id
        mal_item["synonym_name"] = synonym_name
        mal_item["japanese_name"] = japanese_name
        mal_item["english_name"] = english_name
        mal_item["show_type"] = show_type
        mal_item["episodes"] = episodes
        mal_item["status"] = status
        mal_item["airing_start_date"] = airing_start_date
        mal_item["airing_finish_date"] = airing_finish_date
        mal_item["premiered"] = premiered
        mal_item["broadcast"] = broadcast
        mal_item["producers"] = producers
        mal_item["licensors"] = licensors
        mal_item["studios"] = studios
        mal_item["source"] = source
        mal_item["genres"] = genres
        mal_item["themes"] = themes
        mal_item["demographic"] = demographic
        mal_item["duration_in_minutes"] = duration_in_minutes
        mal_item["age_rating"] = age_rating
        mal_item["score"] = score
        mal_item["members"] = members
        mal_item["official_site"] = official_site
        mal_item["anidb_url"] = anidb_url
        mal_item["ann_url"] = ann_url
        mal_item["wikipedia_url"] = wikipedia_url
        mal_item["description"] = description

        yield mal_item
