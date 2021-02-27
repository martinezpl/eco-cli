from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

def scrap_fun_fact():
    try:
        url = 'https://www.beagreatteacher.com/daily-fun-fact/'
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, 'html.parser')
        fun_fact = soup.find('main', class_='content').get_text().split('\n')[6]
        return fun_fact
    except:
        return "<connection failed>"
