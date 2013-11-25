__author__ = 'jnduan'
import codecs
import urllib2
import math
import sys
import json
from bs4 import BeautifulSoup


def fetch_item_list_page(pno):
    itemListUrl = itemListUrlPrefix + str(pno) + itemListUrlSuffix
    print itemListUrl
    itemListHtmlContent = opener.open(itemListUrl).read()
    return itemListHtmlContent


def extract_item_attr(pno):
    itemListHtmlContent = fetch_item_list_page(pno)
    itemListSoup = BeautifulSoup(itemListHtmlContent, from_encoding="gbk")
    pNameDiv = itemListSoup.find_all("div", class_="p-name")
    if pNameDiv:
        for itemUrlDiv in pNameDiv:
            itemUrl = itemUrlDiv.a.get("href")
            print itemUrl
            itemHtmlContent = opener.open(itemUrl).read()
            itemSoup = BeautifulSoup(itemHtmlContent, from_encoding="gbk")
            attrTable = itemSoup.find(id="product-detail-2")
            if attrTable:
                attrDict = {}
                groupName = None
                groupAttrDict = {}
                for attrTR in attrTable.find_all("tr"):
                    tds = list(attrTR.children)
                    if (len(tds)) == 1:
                        if groupName:
                            attrDict[groupName] = groupAttrDict
                        groupName = tds[0].get_text()
                        groupAttrDict = {}
                    elif len(tds) == 2:
                        groupAttrDict[tds[0].get_text()] = tds[1].get_text().replace('\r\n', '')
                attrJSON = json.dumps(attrDict, )
                output_file.write(attrJSON)
                output_file.write("\n")

def main(category_l1, category_l2, category_l3):
    global opener, itemListUrlPrefix, itemListUrlSuffix, output_file, page_size
    opener = urllib2.build_opener()
    page_size = 36.0 #this is a magic number \(-_-)/
    itemListUrlPrefix = 'http://list.jd.com/' + category_l1 + '-' + category_l2 + '-' + category_l3 + '-0-0-0-0-0-0-0-1-1-'
    itemListUrlSuffix = '-1-1-72-33.html'
    output_file_name = '../../output/jditems_attrs_' + category_l3 + '.txt'
    print "save to %s" % (output_file_name)
    output_file = codecs.open(output_file_name, 'w', 'utf-8')

    #fetch 1st page and get the total items count, calc page count.
    itemListFirstPageHtmlContent = fetch_item_list_page(1)
    itemListFirstPageSoup = BeautifulSoup(itemListFirstPageHtmlContent)
    filterDiv = itemListFirstPageSoup.find(id="filter")
    totalDiv = filterDiv.find("div", class_="total")
    itemCount = int(totalDiv.span.strong.get_text())

    pageCount = int(math.ceil(itemCount / page_size))
    print "total %d pages" % (pageCount)
    pass
    for pno in range(1, pageCount + 1):
        extract_item_attr(pno)
    output_file.close()


if __name__ == '__main__':
    if (len(sys.argv) == 4):
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print "usage: python " + sys.argv[0] + " category_l1 cateogry_l2 category_l3"
        sys.exit()