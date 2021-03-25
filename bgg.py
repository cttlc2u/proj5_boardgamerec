import scrapy

class BGG_Spider(scrapy.Spider):
    name = 'bgg'

def start_requests(self):
    for page in range(1,2):
        url = "https://www.boardgamegeek.com/xmlapi2/thing?type=boardgame&id=" + str(page) + "&stats=1&comments=1&pagesize=100"
        yield scrapy.Request(url=url, callback=self.parse)

def parse(self, response):
    #page = response.url.split("=")[-4]
    #filename = f'boardgamegeek-{page}.html'
    filename = 'boardgamegeek_1'
    #with open(filename, 'w') as f:
        #f.write(response.text)
    with open(self.path_to_html, 'w') as html_file:
            html_file.write(response.text)
    self.log(f'Saved file {filename}')
