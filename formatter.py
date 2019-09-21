from datetime import datetime, timedelta

import requests
from lxml import etree
from lxml import html

# Create an html file to output to
file = open("output.html", "wb")

root = etree.Element("html")
head = etree.SubElement(root, "head")
head.append(etree.Element("link", rel="stylesheet", href="css.css", type="text/css"))
body = etree.SubElement(root, "body")
table = etree.SubElement(body, "table", id="table")
header = etree.SubElement(table, "tr")

c1 = etree.SubElement(header, "th")
c2 = etree.SubElement(header, "th")
c3 = etree.SubElement(header, "th")

c1.text = "Match Date"
c2.text = "Teams"
c3.text = "Match Time"

# Get the page from the RWC site and parse it
page = requests.get('https://www.rugbyworldcup.com/matches')
tree = html.fromstring(page.content)

# Get a list of all the match dates
dates = tree.xpath('//div[@class="fixtures__match-date"]')

for date in dates:
    matchDay = date.xpath('div[@class="fixtures-date fixtures__match-day"]')[0]
    day = str(matchDay.xpath('span[@class="fixtures-date__day-number"]/text()')[0])
    month = str(matchDay.xpath('span[@class="fixtures-date__month"]/text()')[0])

    matchDate = str(month.replace(" ", "") + " " + day.replace(" ", "")).replace("\n", "")

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

        datetime = datetime.strptime(localMatchTime, '%H:%M') - timedelta(hours=8)

        teams = match.xpath(teamsXPath)[0].replace(" ", "").replace("\n", " ").strip()

        row = etree.SubElement(table, "tr")

        c1 = etree.SubElement(row, "td")
        c2 = etree.SubElement(row, "td")
        c3 = etree.SubElement(row, "td")

        c1.text = matchDate
        c2.text = teams
        c3.text = datetime.strftime("%H:%M")

file.write(html.tostring(root, pretty_print=True))
