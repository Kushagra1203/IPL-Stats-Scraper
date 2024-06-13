import scrapy
from IPL.items import Team_Items

class TeamResultSpider(scrapy.Spider):
    name = "team_results"
    allowed_domains = ["www.espncricinfo.com"]
    start_urls = ["https://www.espncricinfo.com/records/trophy/team-results-summary/indian-premier-league-117"]

    custom_settings = {
        'FEEDS': {
            'stats/Team_Result.json': {
                'format': 'json',
                'overwrite': True
            }
        }
    }
    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.Teams)
    
    def Teams(self, response):
        rows=response.css('table tbody tr')
        for row in rows:
            team_item=Team_Items()
            team_item['Team']=row.xpath('.//td[1]//text()').get()
            team_item['Playing_Span']=row.xpath('.//td[2]//text()').get()
            team_item['Matches_Played']=row.xpath('.//td[3]//text()').get()
            team_item['Won']=row.xpath('.//td[4]//text()').get()
            team_item['Lost']=row.xpath('.//td[5]//text()').get()
            team_item['Tied_and_Won']=row.xpath('.//td[8]//text()').get()
            team_item['Tied_and_Lost']=row.xpath('.//td[9]//text()').get()
            team_item['No_Result']=row.xpath('.//td[10]//text()').get()
            team_item['Win_Loss_ratio']=row.xpath('.//td[11]//text()').get()
            team_item['Percent_Won']=row.xpath('.//td[12]//text()').get()
            team_item['Percent_Lost']=row.xpath('.//td[13]//text()').get()
            team_item['Result_Percent']=row.xpath('.//td[15]//text()').get()
            
            yield team_item
            
