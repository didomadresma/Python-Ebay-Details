import re
from PyQt4.QtCore import QThread, pyqtSignal
import datetime
from logs.LogManager import LogManager
from utils.Csv import Csv
from utils.Utils import Utils
from spiders.Spider import Spider
from utils.Regex import Regex
from bs4 import BeautifulSoup

__author__ = 'Tuly'


class Scrapper(QThread):
    notifyScrapper = pyqtSignal(object)
    isFinished = False

    def __init__(self, urllist):
        QThread.__init__(self)
        self.logger = LogManager(__name__)
        self.spider = Spider()
        self.regex = Regex()
        self.utils = Utils()
        print urllist
        self.urllist = urllist
        self.csv = Csv('scrapper.csv')

    def run(self):
        self.scrapData()
        self.notifyScrapper.emit(
            '<font color=green><b>------------------ Finish! ------------------------- </b></font>')

    def scrapData(self):
        try:
            total = 0
            csvHeader = ['URL', 'Title', 'Price', 'Brand', 'Features', 'Material', 'Measurements', 'Category',
                         'Size', 'Color', 'Design']
            self.csv.writeCsvRow(csvHeader)
            if self.isFinished: return
            for url in self.urllist:
                if len(url) > 0:
                    url = self.regex.replaceData('(?i)\r', '', url)
                    url = self.regex.replaceData('(?i)\n', '', url)
                    url = self.regex.getSearchedData('(?i)(http.*?)$', url)
                    print 'URL: ', url
                    self.notifyScrapper.emit(('<font color=green><b>URL: %s</b></font>' % url))
                    data = self.spider.fetchData(url)
                    if data and len(data) > 0:
                        data = self.regex.reduceNewLine(data)
                        data = self.regex.reduceBlankSpace(data)
                        soup = BeautifulSoup(data)
                        soup.prettify()
                        title = ''
                        price = ''
                        size = ''
                        brand = ''
                        features = ''
                        material = ''
                        measurements = ''
                        category = ''
                        color = ''
                        design = ''
                        if soup.find('span', id='vi-lkhdr-itmTitl') is not None:
                            title = soup.find('span', id='vi-lkhdr-itmTitl').text
                        if soup.find('span', id='prcIsum'):
                            price = soup.find('span', id='prcIsum').text
                        if soup.find('div', class_='itemAttr'):
                            specchunk = soup.find('div', class_='itemAttr')
                            rows = specchunk.find_all('tr')
                            for row in rows:
                                cols = row.find_all('td')
                                for i in range(0, len(cols), 2):
                                    # if self.regex.isFoundPattern('(?i)Condition:', cols[i].text.strip()):
                                    #     conditionChunk = cols[i + 1]
                                    #     conditionChunk = self.regex.replaceData(u'(?i)<span class="infoLink u-nowrap" id="readFull">.*?</span>', '', unicode(conditionChunk))
                                    #     conditionChunk = self.regex.replaceData(u'(?i)<b class="g-hdn">.*?</b>', '', conditionChunk)
                                    #     condition = BeautifulSoup(conditionChunk).text
                                    #     print condition
                                    if self.regex.isFoundPattern('(?i)Brand:', cols[i].text.strip()):
                                        brand = cols[i + 1].text
                                    if self.regex.isFoundPattern('(?i)Features:', cols[i].text.strip()):
                                        features = cols[i + 1].text
                                    if self.regex.isFoundPattern('(?i)Material:', cols[i].text.strip()):
                                        material = cols[i + 1].text
                                    if self.regex.isFoundPattern('(?i)Measurements:', cols[i].text.strip()):
                                        measurements = cols[i + 1].text
                                    if self.regex.isFoundPattern('(?i)Category:', cols[i].text.strip()):
                                        category = cols[i + 1].text
                                    if self.regex.isFoundPattern('(?i)Color:', cols[i].text.strip()):
                                        color = cols[i + 1].text
                                    if self.regex.isFoundPattern('(?i)Design:', cols[i].text.strip()):
                                        design = cols[i + 1].text
                                    if self.regex.isFoundPattern('(?i)Size:', cols[i].text.strip()):
                                        size = cols[i + 1].text
                        self.notifyScrapper.emit('<font color=black><b>Writting data to csv file.</b></font>')
                        csvData = [url, title, price, brand, features, material, measurements, category, size, color, design]
                        self.notifyScrapper.emit('<font color=black><b>Data: %s</b></font>' % unicode(csvData))
                        self.csv.writeCsvRow(csvData)
                        self.notifyScrapper.emit('<font color=black><b>Successfully Written data to csv file.</b></font>')
                        total += 1
                        self.notifyScrapper.emit('<font color=green><b>Total Data scrapped: [%s]</b></font>' % str(total))
        except Exception, x:
            self.notifyScrapper.emit('<font color=red><b>Error scrapping category: %s</b></font>' % x.message)
            self.logger.error(x.message)
            print x

