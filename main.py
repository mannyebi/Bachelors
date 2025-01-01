from bs4 import BeautifulSoup
import requests


url = "https://www.doostihaa.com/post/1395/10/04/%d8%af%d8%a7%d9%86%d9%84%d9%88%d8%af-%d8%b3%d8%b1%db%8c%d8%a7%d9%84-%d9%84%db%8c%d8%b3%d8%a7%d9%86%d8%b3%d9%87-%d9%87%d8%a7.html"

def find_parts(url):
    """return all parts

    Args:
        url(str): the url you want to scrape.
    """
    html_file = requests.get(url).text
    soup = BeautifulSoup(html_file, 'html.parser')
    first_container = soup.find("div", class_="article_txtc")
    for i in first_container.find_all("p") :
        text = i.text
        if text :
            if "قسمت" in text:
                next_p = i.find_next("p")
                link720 = None
                link480 = None
                for index, a in enumerate(next_p.find_all('a', href=True), start=1):
                    link720 = a['href'] if index == 1 else link720
                    link480 = a['href'] if index == 2 else link480
    return [text, link720, link480]


find_parts(url)


