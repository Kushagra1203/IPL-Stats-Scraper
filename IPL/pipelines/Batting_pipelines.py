# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo

class BattingAvgPipeline:
    
    def __init__(self):
        # Connect to MongoDB
        self.client = pymongo.MongoClient("mongodb+srv://admin:Santosh1210%40@projects.cqzixbp.mongodb.net/")
        # Create or connect to the database
        self.db = self.client["IPL_Stats"]
        # Create or connect to the collection
        self.collection = self.db["batting_avg"]

    def process_item(self, item, spider):
        if spider.name != 'batting_avg':
            return item

        adapter = ItemAdapter(item)
        
        highest_score = adapter.get('highest_score')
        if highest_score:
            highest_score = highest_score.replace('*', '')
            if highest_score.isdigit():
                adapter['highest_score'] = int(highest_score)
            else:
                adapter['highest_score'] = None

        convert_to_int = ['innings_batted', 'not_outs', 'runs', 'hundreds', 'fifties', 'ducks', 'matches_played']

        for field in convert_to_int:
            adapter[field] = int(adapter.get(field, 0))

        convert_to_float = ['batting_average', 'batting_strike_rate']
        
        for field in convert_to_float:
            adapter[field] = float(adapter.get(field, 0.0))

        playing_span = adapter.get('playing_span', '0-0').split('-')
        adapter['start_year'] = int(playing_span[0])
        adapter['last_played_year'] = int(playing_span[1])
        
        adapter.pop('playing_span', None)

        self.collection.update_one(
            {'player': adapter['player'], 'team_name': adapter['team_name']},  # filter
            {'$set': adapter.asdict()},  # update
            upsert=True  # options
        )

        return item


