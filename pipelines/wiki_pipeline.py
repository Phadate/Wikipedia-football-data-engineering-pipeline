def get_wikipedia_page(url, headers):
    import requests
    

    print("getting wikipedia page..", url)


    try:
        response = requests.get(url, headers=headers timeout=10)
        response.raise_for_status() #check if the request is successful
        
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occured: {e}")
        return None
    

def get_wikipedia_data(html):

    from bs4 import BeautifulSoup

    soup =BeautifulSoup(html, "html.parser")
    table = soup.select("table", {"class":"wikitable sortable"})[1]
