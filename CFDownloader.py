import mechanize
from http.cookiejar import CookieJar

from lxml import html
from lxml.html import html5parser as etree
from pyquery import PyQuery as pq

class CFDownloader:
    def __init__(self) -> None:
        self.__cookieJar = CookieJar()
        self.__browser = mechanize.Browser()
        self.__browser.set_handle_robots(False)
        self.__browser.set_cookiejar(self.__cookieJar)

    def login(self, handle, password):
        loginUrl = "https://codeforces.com/enter"
        self.__browser.open("https://codeforces.com/enter")
        self.__browser.select_form(id="enterForm")
        self.__browser.form.find_control(id="handleOrEmail").value = handle
        self.__browser.form.find_control(id="password").value = password
        self.__browser.submit()
    
    def getSourceCode(self, groupId, contestId, submissionId):
        url = f"https://codeforces.com/group/{groupId}/contest/{contestId}/submission/{submissionId}"
        self.__browser.open(url)
        tree2 = html.fromstring(self.__browser.response().read())
        data = etree.fromstring(str(pq(tree2.xpath('//*[@id=\"program-source-text\"]')))).text
        data = data.replace("<pre id=\"program-source-text\" class=\"prettyprint lang-cpp linenums program-source\" style=\"padding: 0.5em;\">","")
        return data