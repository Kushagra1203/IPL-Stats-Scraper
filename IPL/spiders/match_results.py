import scrapy
from IPL.items import Matches_Items
class MatchResultsSpider(scrapy.Spider):
    name = "match_results"
    allowed_domains = ["www.espncricinfo.com","espncricinfo.com"]
    start_urls = ["https://www.espncricinfo.com/records/trophy/team-match-results/indian-premier-league-117"]

    custom_settings = {
        'FEEDS': {
            'Stats/matches_played.json': {
                'format': 'json',
                'overwrite': True
            }
        }
    }
    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.Matches)
    
    def Matches(self, response):
        rows=response.css('table tbody tr')
        for row in rows:
            match_item=Matches_Items()
            match_item['Team_1']=row.xpath('.//td[1]//text()').get()
            match_item['Team_2']=row.xpath('.//td[2]//text()').get()
            match_item['Winner']=row.xpath('.//td[3]//text()').get()
            match_item['Result_Margin']=row.xpath('.//td[4]//text()').get()
            match_item['Ground']=row.xpath('.//td[5]//text()').get()
            match_item['Match_Date']=row.xpath('.//td[6]//text()').get()
        
            yield match_item
            
        