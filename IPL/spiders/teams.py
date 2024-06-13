import scrapy


class BattingAvgSpider(scrapy.Spider):
    name = "teams"
    allowed_domains = ["www.espncricinfo.com"]
    start_urls = ["https://www.espncricinfo.com/records/trophy/indian-premier-league-117"]

    def parse(self, response):
        start_url="https://espncricinfo.com"
        first_ul_element = response.xpath("//div[@class='ds-col-span-2']/following-sibling::div//ul[@class='ds-flex ds-flex-col']")[0]
        teams=first_ul_element.xpath("./li")
        for team in teams:
            yield{
                'name': team.css('a span.ds-grow::text').get(),
                'url': start_url+team.css('a::attr(href)').get()
            }
        
