import mechanize
from http.cookiejar import CookieJar
import time
from urllib.parse import quote

from lxml import html
from lxml.html import html5parser as etree
from pyquery import PyQuery as pq


class CFDownloader:
    def __init__(self) -> None:
        self.__cookieJar = CookieJar()
        self.__browser = mechanize.Browser()
        self.__browser.set_handle_robots(False)
        self.__browser.set_cookiejar(self.__cookieJar)
        self.__browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    def retryMechanize(self, url, timeout):
        proxyurl = "https://api.scrapingant.com/v2/general?url="
        #convert url encode to http encoding
        encoded_url = quote(url)
        proxyurl += encoded_url
        proxyurl += "&x-api-key=718a20a35d174225904cf787680ddc6c"


        error_occured = False
        try: 
            self.__browser.open(url, timeout=timeout)
        except mechanize.URLError:
            error_occured = True
        while error_occured:
            try:
                self.__browser.open(proxyurl, timeout=timeout)
                error_occured = False
            except mechanize.URLError:
                error_occured = True
                print("Error occured, retrying after 30 seconds...")
                time.sleep(30)
        

    def login(self, handle, password):
        loginUrl = "https://codeforces.com/enter"
        self.retryMechanize(loginUrl, 10)
        self.__browser.select_form(id="enterForm")
        self.__browser.form.find_control(id="handleOrEmail").value = handle
        self.__browser.form.find_control(id="password").value = password
        self.__browser.submit()
    
    def getSourceCode(self, groupId, contestId, submissionId):
        data = ""
        try:
            url = f"https://codeforces.com/group/{groupId}/contest/{contestId}/submission/{submissionId}"
            self.retryMechanize(url, 10)
            tree2 = html.fromstring(self.__browser.response().read())
            data = etree.fromstring(str(pq(tree2.xpath('//*[@id=\"program-source-text\"]'))))
            data = data.text
            data = data.replace("<pre id=\"program-source-text\" class=\"prettyprint lang-cpp linenums program-source\" style=\"padding: 0.5em;\">","")
        except:
            data = ""
        return data
    
