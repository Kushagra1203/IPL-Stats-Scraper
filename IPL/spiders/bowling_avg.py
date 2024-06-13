import scrapy
from IPL.items import Bowling_Items


class BowlingAvgSpider(scrapy.Spider):
    name = "bowling_avg"
    allowed_domains = ["espncricinfo.com", "www.espncricinfo.com"]
    start_urls = ["https://www.espncricinfo.com/records/trophy/indian-premier-league-117"]

    custom_settings = {
        'FEEDS': {
            'Stats/bowling_avg.csv': {
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
        first_ul_element = response.xpath("//div[@class='ds-col-span-2']/following-sibling::div//ul[@class='ds-flex ds-flex-col']")[1]
        teams=first_ul_element.xpath("./li")
        for team in teams:
            team_name= team.css('a span.ds-grow::text').get()
            team_url= start_url+team.css('a::attr(href)').get()
            yield scrapy.Request(team_url, callback=self.team_players, meta={'team_name': team_name})
    
    def team_players(self,response):
        team_name = response.meta['team_name']
        rows=response.css('table tbody tr')
        for row in rows:
            player_item = Bowling_Items()
            player_item['team_name'] = team_name
            player_item['player'] = row.xpath('.//td[1]//text()').get()
            player_item['playing_span'] = row.xpath('.//td[2]//text()').get()
            player_item['matches_played'] = row.xpath('.//td[3]//text()').get()
            player_item['innings_bowled'] = row.xpath('.//td[4]//text()').get()
            player_item['balls'] = row.xpath('.//td[5]//text()').get()
            player_item['maidens_earned'] = row.xpath('.//td[6]//text()').get()
            player_item['runs_conceded'] = row.xpath('.//td[7]//text()').get()
            player_item['wickets'] = row.xpath('.//td[8]//text()').get()
            player_item['best_innings_bowled'] = row.xpath('.//td[9]//text()').get()
            player_item['bowling_average'] = row.xpath('.//td[10]//text()').get()
            player_item['economy_rate'] = row.xpath('.//td[11]//text()').get()
            player_item['bowling_stike_rate'] = row.xpath('.//td[12]//text()').get()
            player_item['catches_taken'] = row.xpath('.//td[15]//text()').get()
            
            yield player_item
            

