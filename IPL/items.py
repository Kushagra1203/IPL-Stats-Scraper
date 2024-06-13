# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import scrapy.item


class IplItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Batting_Items(scrapy.Item):
    team_name=scrapy.Field()
    player=scrapy.Field()
    matches_played=scrapy.Field()
    playing_span = scrapy.Field()
    innings_batted=scrapy.Field()
    not_outs=scrapy.Field()
    runs=scrapy.Field()
    highest_score=scrapy.Field()
    batting_average=scrapy.Field()
    batting_strike_rate=scrapy.Field()
    hundreds=scrapy.Field()  
    fifties=scrapy.Field() 
    ducks=scrapy.Field()  
    start_year = scrapy.Field()  
    last_played_year = scrapy.Field()  
    
class Bowling_Items(scrapy.Item):
    team_name=scrapy.Field()
    player=scrapy.Field()
    matches_played=scrapy.Field()
    playing_span = scrapy.Field()
    innings_bowled=scrapy.Field()
    balls=scrapy.Field()
    maidens_earned=scrapy.Field()
    runs_conceded=scrapy.Field()
    wickets=scrapy.Field()
    best_innings_bowled=scrapy.Field()
    bowling_average=scrapy.Field()
    economy_rate=scrapy.Field()
    bowling_stike_rate=scrapy.Field()
    best_innings_bowled_wickets=scrapy.Field()
    best_innings_bowled_runs=scrapy.Field()
    catches_taken=scrapy.Field()
    start_year = scrapy.Field()  
    last_played_year = scrapy.Field()  
    
class Matches_Items(scrapy.Item):
    Team_1=scrapy.Field()
    Team_2=scrapy.Field()
    Winner=scrapy.Field()
    Result_Margin=scrapy.Field()
    Ground=scrapy.Field()
    Match_Date=scrapy.Field()
    Season=scrapy.Field()
    result_margin_value=scrapy.Field()
    result_margin_type=scrapy.Field()

class Team_Items(scrapy.Item):
    Team=scrapy.Field()
    Playing_Span=scrapy.Field()
    Matches_Played=scrapy.Field()
    Won=scrapy.Field()
    Lost=scrapy.Field()
    Tied_and_Won=scrapy.Field()
    Tied_and_Lost=scrapy.Field()
    No_Result=scrapy.Field()
    Win_Loss_ratio=scrapy.Field()
    Percent_Won=scrapy.Field()
    Percent_Lost=scrapy.Field()
    Result_Percent=scrapy.Field()
    start_year=scrapy.Field()
    last_played_year=scrapy.Field()