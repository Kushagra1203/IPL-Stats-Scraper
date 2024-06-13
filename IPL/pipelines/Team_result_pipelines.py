# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
import os 

class TeamsPipeline:
    def __init__(self):
        # Connect to MongoDB
        self.client = pymongo.MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
        # Create or connect to the database
        self.db = self.client["IPL_Stats"]
        # Create or connect to the collection
        self.collection = self.db["team_results"]
        
    def process_item(self, item, spider):

        if spider.name != 'team_results':
            return item
        
        adapter = ItemAdapter(item)
        
        playing_span = adapter.get('Playing_Span').split('-')
        adapter['start_year'] = int(playing_span[0])
        adapter['last_played_year'] = int(playing_span[1])

        adapter.pop('Playing_Span', None)
        
        convert_to_int=['Matches_Played', 'Won', 'Lost', 'Tied_and_Won', 'Tied_and_Lost', 'No_Result']
        for field in convert_to_int:
            adapter[field]=int(adapter.get(field,0))
            
        convert_to_float=['Win_Loss_ratio', 'Percent_Won', 'Percent_Lost', 'Result_Percent']
        for field in convert_to_float:
            adapter[field]=float(adapter.get(field,0.0))

        self.collection.update_one(
            {'Team': adapter['Team']},  # filter
            {'$set': adapter.asdict()},  # update
            upsert=True  # options
        )

        return item
