import requests
from bs4 import BeautifulSoup

def get_wikipedia_page(url, headers):
    print(f"Fetching Wikipedia page: {url}")
    if not headers.get("User-Agent"):
        headers["User-Agent"] = "MyWikipediaBot/1.0 (fayoded@gmail.com)"
    
    try:
        response = requests.get(url, headers=headers, timeout=30) 
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    

def get_wikipedia_data(html):
    if not html:
        print("No HTML content provided")
        return None
    
    try:
        soup = BeautifulSoup(html, "html.parser")
        tables = soup.select("table", {"class": "wikitable sortable"})
        if len(tables) < 2:
            print("Fewer than 2 sortable tables found")
            return None
        table = tables[1]
        table_rows = table.find_all('tr')
        return table_rows
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return None


def extract_wikipedia_data(**kwargs):
    url = kwargs.get('url')
    headers = kwargs.get('headers', {})
    html = get_wikipedia_page(url, headers=headers) 
    rows = get_wikipedia_data(html)
    print(rows)
    return rows  