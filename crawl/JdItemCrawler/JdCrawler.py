__author__ = 'jnduan'
import codecs
import urllib2
import json
from bs4 import BeautifulSoup
opener = urllib2.build_opener()
itemListUrlPrefix = 'http://list.jd.com/670-671-672-0-0-0-0-0-0-0-1-1-'
itemListUrlSuffix = '-1-1-72-4137-33.html'
output_file = codecs.open('/Users/jnduan/temp/jditems.txt', 'w', 'utf-8')
for pno in range(1, 19):
    itemListUrl = itemListUrlPrefix + str(pno) + itemListUrlSuffix
    print itemListUrl
    itemListHtmlContent = opener.open(itemListUrl).read()
    itemListSoup = BeautifulSoup(itemListHtmlContent)
    pNameDiv = itemListSoup.find_all("div", class_="p-name")
    if pNameDiv:
        for itemUrlDiv in pNameDiv:
            itemUrl = itemUrlDiv.a.get("href")
            print itemUrl
            itemHtmlContent = opener.open(itemUrl).read()
            itemSoup = BeautifulSoup(itemHtmlContent)
            attrTable = itemSoup.find(id="product-detail-2")
            if attrTable:
                attrDict = {}
                for attrTR in attrTable.find_all("tr"):
                    td = attrTR.find_all("td")
                    if len(td) == 2:
                        attrDict[td[0].get_text()] = td[1].get_text()
                attrJSON = json.dumps(attrDict)
                output_file.write(attrJSON.decode("unicode-escape"))
                output_file.write("\n")
output_file.close()