from bs4 import BeautifulSoup
import requests
import typer
from rich.console import Console
import webbrowser
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type



url = "https://www.doostihaa.com/post/1395/10/04/%d8%af%d8%a7%d9%86%d9%84%d9%88%d8%af-%d8%b3%d8%b1%db%8c%d8%a7%d9%84-%d9%84%db%8c%d8%b3%d8%a7%d9%86%d8%b3%d9%87-%d9%87%d8%a7.html"

app = typer.Typer()
console = Console()


triggered_keys = set()
current_col = 1

@app.command()
def hello(name: str):
    print(f"Hello {name}")


def look_for_keys(*keys, text):
    """Look for a special key in a text.

    Args:
        keys: The keys you want to be in the text
        text: The text in which to search for the keys
    """
    for key in keys:
        if key not in text:
            return False
    return True



@retry(
    stop=stop_after_attempt(3),                # Retry up to 3 times
    wait=wait_exponential(multiplier=1, min=2, max=10),  # Exponential backoff
    retry=retry_if_exception_type(requests.exceptions.RequestException),  # Retry for specific exceptions
)
def fetch_data(url):
    """send's get request to url and handle error and retry mechanism
    """
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response
    

def make_soup(html_file):
    """return the soup which beautifulsoup makes it.

    Args:
        html_file(text): the html file that you wanna do things with it.
    """
    soup = BeautifulSoup(html_file, 'html.parser')
    return soup


def find_parts(url):
    """return all parts

    Args:
        url(str): the url you want to scrape.
    """
    result = []
    try:
        html_file = fetch_data(url).text #with retry mechanism
    except Exception as e:
        print(f"an error occured :( -> {e}")

    soup = make_soup(html_file)

    try:
        first_container = soup.find("div", class_="article_txtc")
    except Exception as e:
        print(e)
    else:
        if first_container is None:
            print('the data was not found :(')
            return
        
    for i in first_container.find_all("p") :
        text = i.text
        if text :
            if look_for_keys("قسمت", "دانلود", text=text):
                next_p = i.find_next("p")
                link720 = None
                link480 = None
                for index, a in enumerate(next_p.find_all('a', href=True), start=1):
                    link720 = a['href'] if index == 1 else link720
                    link480 = a['href'] if index == 2 else link480
                result.append([text, link720, link480])
    return result


@app.command()
def download():
    """show the list of series parts.

    Args:
        series_list(list): a list of parts conatin's part, download link for 720p quality and 480p quality.
    """
    global current_col
    try : 
        series_list = find_parts(url)
    except:
        console.print("couldn't load data !", style="red")
        return
    else:
        if series_list is None:
            return
    for i in series_list:
        console.print(f"> {i[0][1:-1]}", style="blue")
        # link720 = i[1]
        # link480 = i[2]
    print("\n")
    part = typer.prompt("Enter the part you want to download ")
    webbrowser.open(series_list[int(part)-1][1])



if __name__ == "__main__":
    app()