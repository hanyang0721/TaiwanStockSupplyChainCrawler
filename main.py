import seleniumclass as sele
from bs4 import BeautifulSoup
import DBconnect
import re

crawllist = []
baseurl = 'https://pchome.megatime.com.tw'
database = None


def parseStockList(bsobj, category):
    for x in range(0, bsobj.find_all('td').__len__(), 10):
        stockname = bsobj.find_all('td')[x].string
        stockidx = re.search("\((\w+)\)", bsobj.find_all('td')[x].string)[1]
        print(category['Key'], stockname, stockidx)
        database.InsertStockCategory(category['Key'], stockname, stockidx)


def chkfornextpage(soup):
    for page in soup.find("div", class_='pages').find_all('a'):
        if page.contents[0] == '下一頁':
            return page.get('href')
    return ''


def prepareCrawlList(crawlurl, bsobj):
    global crawllist
    del crawllist[:]
    if crawlurl == 'https://pchome.megatime.com.tw/group/sto3':
        for link in bsobj:  # get all the categories
            crawllist.append({'Key': link.string, 'Link': link.get('href')})  # link.get('href')
    elif crawlurl == 'https://pchome.megatime.com.tw/group/':
        for i in range(1, bsobj.__len__(), 1):  # skip 成份股報價
            for link in bsobj[i].find_all('a'):
                crawllist.append({'Key': link.string, 'Link': link.get('href')})  # link.get('href')


def crawlStockList(driver, url):
    global crawllist
    count = 0
    bsobj = None
    htmltext = driver.GetHtmlsource(url)
    soup = BeautifulSoup(htmltext, "html.parser")
    if url == 'https://pchome.megatime.com.tw/group/sto3':
        bsobj = soup.find("div", class_='catoli').find_all('a')
    elif url == 'https://pchome.megatime.com.tw/group/':
        bsobj = soup.find_all("div", class_='catoli')
    prepareCrawlList(url, bsobj)
    print('Total categoreis %d' % crawllist.__len__())
    for i in crawllist:
        if i['Key'] == '權證':
            continue
        print('Current Category No: ' + str(count) + ', Category Name: ' + i['Key'])
        count += 1
        url = baseurl + i['Link']
        htmltext = driver.GetHtmlsource(url)
        soup = BeautifulSoup(htmltext, "html.parser")
        bsobj = soup.find("tbody", {"id": "cpidStock"})
        try:
            parseStockList(bsobj, i)
            # Next page exists
            nextpageurl = chkfornextpage(soup)
            pageno = 2
            while nextpageurl != '':
                print('category name: ' + i['Key'] + ' ,page No. ' + str(pageno))
                pageno += 1
                htmltext = driver.GetHtmlsource(baseurl + nextpageurl)
                soup = BeautifulSoup(htmltext, "html.parser")
                bsobj = soup.find("tbody", {"id": "cpidStock"})
                parseStockList(bsobj, i)
                nextpageurl = chkfornextpage(soup)
        except AttributeError as ex:
            print(str(ex))




def main():
    global database
    database = DBconnect.DBconnect('localhost', 'Stock', 'trader', 'trader')
    database.Connect()
    driver = sele.MyseleniumClass()
    crawlStockList(driver, 'https://pchome.megatime.com.tw/group/sto3')
    crawlStockList(driver,  'https://pchome.megatime.com.tw/group/')


if __name__ == "__main__":
    main()
