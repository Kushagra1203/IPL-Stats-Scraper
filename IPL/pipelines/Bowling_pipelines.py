# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo

class BowlingAvgPipeline:
    
    def __init__(self):
        # Connect to MongoDB
        self.client = pymongo.MongoClient("mongodb+srv://admin:Santosh1210%40@projects.cqzixbp.mongodb.net/")
        # Create or connect to the database
        self.db = self.client["IPL_Stats"]
        # Create or connect to the collection
        self.collection = self.db["bowling_avg"]
        
        
    def process_item(self, item, spider):
        if spider.name != 'bowling_avg':
            return item

        adapter = ItemAdapter(item)

        best_innings_bowled = adapter.get('best_innings_bowled')
        if best_innings_bowled:
            best_innings_bowled = best_innings_bowled.replace('*', '')
            if '/' in best_innings_bowled:
                best_innings_bowled = best_innings_bowled.split('/')
                adapter['best_innings_bowled_wickets'] = int(best_innings_bowled[0])
                adapter['best_innings_bowled_runs'] = int(best_innings_bowled[1])
            else:
                adapter['best_innings_bowled_wickets'] = None
                adapter['best_innings_bowled_runs'] = None

        convert_to_int = ['innings_bowled', 'balls', 'maidens_earned', 'runs_conceded', 'wickets', 'matches_played', 'catches_taken']

        for field in convert_to_int:
            adapter[field] = int(adapter.get(field, 0))

        convert_to_float = ['bowling_average', 'economy_rate', 'bowling_stike_rate']

        for field in convert_to_float:
            if adapter.get(field) == '-':
                adapter[field] = None
            else:
                adapter[field] = float(adapter.get(field, 0.0))

        playing_span = adapter.get('playing_span', '0-0').split('-')
        adapter['start_year'] = int(playing_span[0])
        adapter['last_played_year'] = int(playing_span[1])

        adapter.pop('playing_span', None)
        adapter.pop('best_innings_bowled', None)

        self.collection.update_one(
            {'player': adapter['player'], 'team_name': adapter['team_name']},  # filter
            {'$set': adapter.asdict()},  # update
            upsert=True  # options
        )
        return item

       
