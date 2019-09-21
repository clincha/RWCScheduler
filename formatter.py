import os

from lxml import html
import requests

# Get the page from the RWC site and parse it
page = requests.get('https://www.rugbyworldcup.com/matches')
tree = html.fromstring(page.content)

# Create file with contents of web page for debugging
os.remove("page.html")
file = open("page.html", "wb")
file.write(page.content)
file.close()

# Get a list of all the match dates
dates = tree.xpath('//div[@class="fixtures__match-date"]')

for date in dates:
    matchDay = date.xpath('div[@class="fixtures-date fixtures__match-day"]')[0]
    day = str(matchDay.xpath('span[@class="fixtures-date__day-number"]/text()')[0])
    month = str(matchDay.xpath('span[@class="fixtures-date__month"]/text()')[0])

    print(str(month.replace(" ", "") + " " + day.replace(" ", "")).replace("\n", ""))

    matches = date.xpath('div[contains(@class,"fixtures__match-wrapper")]')
    for match in matches:
        matchTimeXPath = 'div[@class="fixtures__match"]' \
                         '/span[@class="fixtures__match-content"]' \
                         '/div[@class="fixtures__match-meta"]' \
                         '/div[@class="fixtures__match-times"]' \
                         '/div[@class="fixtures__time fixtures__time--local-time"]' \
                         '/span' \
                         '/text()'

        teamsXPath = 'div[@class="fixtures__match"]' \
                     '/span[@class="fixtures__match-content"]' \
                     '/div[@class="fixtures__match-info-container"]' \
                     '/div[@class="fixtures__match-info"]' \
                     '/a[@class="fixtures__match-link--info"]' \
                     '/div[@class="fixtures__teams"]' \
                     '/text()'

        localMatchTime = match.xpath(matchTimeXPath)[0]
        print(localMatchTime)

        teams = match.xpath(teamsXPath)[0]
        print(str(teams).replace(" ", "").replace("\n", " ").lstrip())
