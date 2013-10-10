__author__ = 'jnduan'
import codecs
import urllib2
import json
from bs4 import BeautifulSoup
opener = urllib2.build_opener()
itemListUrlPrefix = 'http://www.newegg.com.cn/SubCategory/970-'
itemListUrlSuffix = '.htm#itemGrid1'
output_file = codecs.open('../../output/xditems.txt', 'w', 'utf-8')
for pno in range(1, 5):
    itemListUrl = itemListUrlPrefix + str(pno) + itemListUrlSuffix
    print itemListUrl
    itemListHtmlContent = opener.open(itemListUrl).read()
    itemListSoup = BeautifulSoup(itemListHtmlContent)
    itemListLi = itemListSoup.find_all("li", class_="cls")
    if itemListLi:
        for itemLi in itemListLi:
            aWrap = itemLi.find_all("p", class_="title")
            if aWrap:
                itemUrl = aWrap[0].a.get("href")
                print itemUrl
                itemHtmlContent = opener.open(itemUrl).read()
                itemSoup = BeautifulSoup(itemHtmlContent)
                attrTable = itemSoup.find(id="tabCot_product_2")
                if attrTable:
                    attrDict = {}
                    for attrTR in attrTable.find_all("tr"):
                        if len(list(attrTR.children)) == 2:
                            attrDict[attrTR.th.get_text()] = attrTR.td.get_text()
                    attrJSON = json.dumps(attrDict)
                    output_file.write(attrJSON.decode("unicode-escape"))
                    output_file.write("\n")
output_file.close()