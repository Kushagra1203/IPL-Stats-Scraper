import scrapy
from IPL.items import Batting_Items

class batting_avg(scrapy.Spider):
    name = "batting_avg"
    allowed_domains = ["espncricinfo.com", "www.espncricinfo.com"]
    start_urls = ["https://www.espncricinfo.com/records/trophy/indian-premier-league-117"]
    
    custom_settings = {
        'FEEDS': {
            'Stats/batting_avg.csv': {
                'format': 'csv',
                'overwrite': True
            }
        }
    }
    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.team)
    
    def team(self, response):
        start_url="https://espncricinfo.com"
        first_ul_element = response.xpath("//div[@class='ds-col-span-2']/following-sibling::div//ul[@class='ds-flex ds-flex-col']")[0]
        teams=first_ul_element.xpath("./li")
        for team in teams:
            team_name= team.css('a span.ds-grow::text').get()
            team_url= start_url+team.css('a::attr(href)').get()
            yield scrapy.Request(team_url, callback=self.team_players, meta={'team_name': team_name})
        
    def team_players(self,response):
        team_name = response.meta['team_name']
        rows=response.css('table tbody tr')
        for row in rows:
            player_item = Batting_Items()
            player_item['team_name'] = team_name
            player_item['player'] = row.xpath('.//td[1]//text()').get()
            player_item['playing_span'] = row.xpath('.//td[2]//text()').get()
            player_item['matches_played'] = row.xpath('.//td[3]//text()').get()
            player_item['innings_batted'] = row.xpath('.//td[4]//text()').get()
            player_item['not_outs'] = row.xpath('.//td[5]//text()').get()
            player_item['runs'] = row.xpath('.//td[6]//text()').get()
            player_item['highest_score'] = row.xpath('.//td[7]//text()').get()
            player_item['batting_average'] = row.xpath('.//td[8]//text()').get()
            player_item['batting_strike_rate'] = row.xpath('.//td[9]//text()').get()
            player_item['hundreds'] = row.xpath('.//td[10]//text()').get()
            player_item['fifties'] = row.xpath('.//td[11]//text()').get()
            player_item['ducks'] = row.xpath('.//td[12]//text()').get()
            yield player_item
        
