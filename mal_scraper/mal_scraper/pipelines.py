# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MalScraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # remove \n then whitespaces and then \r from every item
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            if value:
                value = value.replace("\n", "")
                value = value.strip()
                value = value.replace("\r", "")
                adapter[field_name] = value

        # converting mal_id, episodes, members to int
        int_conversion_keys = ["mal_id", "members", "episodes"]
        for key in int_conversion_keys:
            value = adapter.get(key).replace(",", "")
            if value:
                value = int(value)
                adapter[key] = value

        score_value = adapter.get("score")
        if score_value != "N/A":
            score_value = float(score_value)
        else:
            score_value = None
        adapter["score"] = score_value

        # converting items to list
        items_to_convert = ["producers", "licensors", "studios","genres", "themes"]
        for item_to_convert in items_to_convert:
            value = adapter.get(item_to_convert)
            if value:
                value = value.split(",")
                value = [i.strip() for i in value]
                if item_to_convert in ["genres", "themes"]:
                    value = [i.lower() for i in value]
            adapter[item_to_convert] = value

        duration_value = adapter.get("duration_in_minutes")
        if duration_value:
            duration_value = int(duration_value.split(" ")[0].strip())
            adapter["duration_in_minutes"] = duration_value

        return item
