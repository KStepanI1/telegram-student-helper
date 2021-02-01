import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
}
URL = 'https://etu.ru/'


class HtmlStatusCodeError(Exception):
    pass


class StatusOfTheWeek:
    async def get_html(self, url, params=None):
        response = requests.get(url=url, headers=HEADERS, params=params)
        return response

    async def get_content(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        item = soup.find('div', class_='btn btn-default btn-sm date')
        return item.get_text()

    async def parse(self):
        html = await self.get_html(URL)
        if html.status_code == 200:
            result = await self.get_content(html.text)
            return result
        else:
            raise HtmlStatusCodeError

