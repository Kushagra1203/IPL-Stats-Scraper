# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo

class TeamsPipeline:
    
        
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
        
        return item