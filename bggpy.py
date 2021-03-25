import requests
import time
import random
from fake_useragent import UserAgent

pages = []
for i in range(0,51):
    pages.append(i)

for batch in range(1,20001):
    ua = UserAgent()
    user_agent = {'User-agent': ua.random}
    url = "https://www.boardgamegeek.com/xmlapi2/thing?type=boardgame&id="+str(pages)+"&stats=1&comments=1&pagesize=100"
    response = requests.get(url, headers = user_agent)
    filename = "bgg_firstthousand_" + str(batch) + ".txt"
    with open(filename, "w") as f:
        f.write(response.text)
    time.sleep(5+2*random.random())
    pages = list(map(lambda m : m + 50, pages))
