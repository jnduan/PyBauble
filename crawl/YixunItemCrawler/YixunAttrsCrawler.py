#coding:utf8
__author__ = 'jnduan'
import codecs
import urllib2
import math
import sys
import json
import re
from bs4 import BeautifulSoup


def fetch_item_list_page(pno):
    itemListUrl = itemListUrlPrefix + str(pno) + itemListUrlSuffix
    print itemListUrl
    itemListHtmlContent = opener.open(itemListUrl).read()
    return itemListHtmlContent


def extract_item_attr(pno):
    itemListHtmlContent = fetch_item_list_page(pno)
    itemListSoup = BeautifulSoup(itemListHtmlContent, from_encoding="utf-8")
    itemListLi = itemListSoup.find_all("li", class_="goods_li")
    if itemListLi:
        for itemLi in itemListLi:
            aWrap = itemLi.find_all("p", class_="mod_goods_tit")
            if aWrap:
                itemUrl = aWrap[0].a.get("href")
                print itemUrl
                itemHtmlContent = opener.open(itemUrl).read()
                detailUrlMatcher = re.findall(detailUrlRe, itemHtmlContent, re.S)
                for detUrl in detailUrlMatcher:
                    print detUrl
                    detailRsps = opener.open(detUrl).read()
                    detailMatcher = re.findall(detailRspsRe, detailRsps, re.S)
                    for detailHtml in detailMatcher:
                        attrTable = BeautifulSoup(detailHtml, from_encoding="utf-8")
                        if attrTable:
                            attrDict = {}
                            for attrTR in attrTable.find_all("tr"):
                                tds = list(attrTR.children)
                                if len(tds) == 2:
                                    attrDict[tds[0].get_text()] = tds[1].get_text().replace('\\r', '').replace('\\n', '')
                            attrJSON = json.dumps(attrDict)
                            output_file.write(attrJSON)
                            output_file.write("\n")


def main(category_l1, category_l2):
    global opener, itemListUrlPrefix, itemListUrlSuffix, output_file, page_size, detailUrlRe, detailRspsRe
    #var config = {detailUrl: 'http://item.wgimg.com/det_000000000000000000000051789EC28B',lv: '524287'};
    detailUrlRe = r'(http://item\.wgimg\.com/det_[0-9A-Z]{32})'
    detailRspsRe = r'"1":"(<TABLE.*?</TABLE>)",'
    opener = urllib2.build_opener()
    page_size = 40.0 #this is a magic number \(-_-)/
    itemListUrlPrefix = 'http://searchex.yixun.com/html?path=' + category_l1 + 't' + category_l2 + '&page='
    itemListUrlSuffix = ''
    output_file_name = '../../output/yxitems_attrs_' + category_l1 + '_' + category_l2 + '.txt'
    print "save to %s" % (output_file_name)
    output_file = codecs.open(output_file_name, 'w', 'utf-8')

    #fetch 1st page and get the total items count, calc page count.
    itemListFirstPageHtmlContent = fetch_item_list_page(1)
    itemListFirstPageSoup = BeautifulSoup(itemListFirstPageHtmlContent)
    pageNavRecordsDiv = itemListFirstPageSoup.find("div", class_="sort_page_txt")
    totalEm = pageNavRecordsDiv.find("b")
    itemCount = int(totalEm.get_text())

    pageCount = int(math.ceil(itemCount / page_size))
    print "total %d pages" % (pageCount)
    pass
    for pno in range(1, pageCount + 1):
        extract_item_attr(pno)
    output_file.close()


if __name__ == '__main__':
    if (len(sys.argv) == 3):
        main(sys.argv[1], sys.argv[2])
    else:
        print "usage: python " + sys.argv[0] + " category_l1 category_l2"
        sys.exit()
