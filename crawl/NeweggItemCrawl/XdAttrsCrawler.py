#coding:utf8
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
    itemListSoup = BeautifulSoup(itemListHtmlContent, from_encoding="gb2312")
    itemListLi = itemListSoup.find_all("li", class_="cls")
    if itemListLi:
        for itemLi in itemListLi:
            aWrap = itemLi.find_all("p", class_="title")
            if aWrap:
                itemUrl = aWrap[0].a.get("href")
                print itemUrl
                itemHtmlContent = opener.open(itemUrl).read()
                itemSoup = BeautifulSoup(itemHtmlContent, from_encoding="gb2312")
                attrTable = itemSoup.find(id="tabCot_product_2")
                if attrTable:
                    attrDict = {}
                    for attrTR in attrTable.find_all("tr"):
                        if len(list(attrTR.children)) == 2:
                            attrDict[attrTR.th.get_text()] = attrTR.td.get_text().replace('\r\n', '')
                    attrJSON = json.dumps(attrDict)
                    output_file.write(attrJSON.decode("unicode-escape"))
                    output_file.write("\n")


def main(category_id):
    global opener, itemListUrlPrefix, itemListUrlSuffix, output_file, page_size
    opener = urllib2.build_opener()
    page_size = 24.0 #this is a magic number \(-_-)/
    itemListUrlPrefix = 'http://www.newegg.com.cn/SubCategory/'+category_id+'-'
    itemListUrlSuffix = '.htm#itemGrid1'
    output_file_name = '../../output/xditems_attrs_' + category_id + '.txt'
    print "save to %s" % (output_file_name)
    output_file = codecs.open(output_file_name, 'w', 'utf-8')

    #fetch 1st page and get the total items count, calc page count.
    itemListFirstPageHtmlContent = fetch_item_list_page(1)
    itemListFirstPageSoup = BeautifulSoup(itemListFirstPageHtmlContent)
    pageNavRecordsSpan = itemListFirstPageSoup.find("span", class_="pageNav_records")
    totalEm = pageNavRecordsSpan.find("em", class_="gold")
    itemCount = int(totalEm.get_text())

    pageCount = int(math.ceil(itemCount / page_size))
    print "total %d pages" % (pageCount)
    pass
    for pno in range(1, pageCount + 1):
        extract_item_attr(pno)
    output_file.close()


if __name__ == '__main__':
    if (len(sys.argv) == 2):
        main(sys.argv[1])
    else:
        print "usage: python " + sys.argv[0] + " category_id"
        sys.exit()
