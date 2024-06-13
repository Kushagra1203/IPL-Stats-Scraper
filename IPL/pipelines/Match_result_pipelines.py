# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime
import pymongo

class MatchesPipeline:
    
    def __init__(self):
        # Replace 'username', 'password', 'your-cluster-url', 'your-database', and 'your-collection' with your actual values
        # Connect to MongoDB
        self.client = pymongo.MongoClient("mongodb+srv://username:password@your-cluster-url")
        # Create or connect to the database
        self.db = self.client["your-database"]
        # Create or connect to the collection
        self.collection = self.db["your-collection"]
        # Create a dictionary that maps the short forms to the full forms
        self.team_names = {
            'CSK': 'Chennai Super Kings',
            'DC': 'Delhi Capitals',  
            'Daredevils': 'Delhi Daredevils', 
            'KKR': 'Kolkata Knight Riders',
            'MI': 'Mumbai Indians',
            'Kings XI': 'Kings XI Punjab',  
            'RCB': 'Royal Challengers Bangalore',
            'RR': 'Rajasthan Royals',
            'SRH': 'Sunrisers Hyderabad',
            'Chargers': 'Deccan Chargers',  
            'Warriors': 'Pune Warriors India',  
            'Guj Lions': 'Gujarat Lions',  
            'Supergiants': 'Rising Pune Supergiant',  
            'Kochi': 'Kochi Tuskers Kerala', 
            'GT': 'Gujarat Titans',  
            'LSG': 'Lucknow Super Giants',  
        }

    
    def process_item(self, item, spider):
        
        if spider.name != 'match_results':
            return item
        
        adapter = ItemAdapter(item)
        
        match_date_str = adapter.get('Match_Date')
        if '-' in match_date_str:
            match_date_str = match_date_str.split('-')[0] + match_date_str[-6:]
        match_date = datetime.strptime(match_date_str, '%b %d, %Y')
        year = match_date.year
        adapter['Season'] = year
        
        fields=['Team_1','Team_2','Winner']
        for field in fields:
            short_form = adapter.get(field)
            adapter[field] = self.team_names.get(short_form, short_form)
            
        # Split the result_margin into value and type
        result_margin = adapter.get('Result_Margin')
        if result_margin:
            result_margin_value, result_margin_type = result_margin.split(' ')
            adapter['result_margin_value'] = int(result_margin_value)
            adapter['result_margin_type'] = result_margin_type
        
        self.collection.update_one(
            {'Match_Date': adapter['Match_Date'], 'Team_1': adapter['Team_1'], 'Team_2': adapter['Team_2']},  # filter
            {'$set': adapter.asdict()},  # update
            upsert=True  # options
        )
        
        return item
