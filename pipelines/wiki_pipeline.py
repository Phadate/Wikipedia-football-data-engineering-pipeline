import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from geopy.geocoders import Nominatim
from datetime import datetime
from time import sleep
import os


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

def clean_text(text):
    text = str(text).strip()
    if text.find("\xa0"):
        text = text.split("\xa0")[0]
    if text.find(" ♦"):
        text = text.split(" ♦")[0]
    if text.find('[') != -1:
        text =text.split('[')[0]
    
    return text.replace('\n', '')

def extract_wikipedia_data(**kwargs):
    url = kwargs.get('url')
    headers = kwargs.get('headers', {})
    html = get_wikipedia_page(url, headers=headers) 
    table_rows = get_wikipedia_data(html)
    

    data = []

    for i in range(1, len(table_rows)):
        tds = table_rows[i].find_all('td')
        values = {
            'Rank' : i,
            'Stadium' : clean_text(tds[0].text),
            'Seating capacity' : clean_text(tds[1].text),
            'Region' : clean_text(tds[2].text),
            'Country' : clean_text(tds[3].text),
            'City' : clean_text(tds[4].text),
            'Images' : (('https://' + tds[5].find('img').get('src').split("//")[1])  if tds[5].find('img') and tds[5].find('img').get('src') else "No image available"),
            'Home_Team' : clean_text(tds[6].text)
        }

        data.append(values)
    json_rows =json.dumps(data)
    kwargs['ti'].xcom_push(key='rows', value=json_rows)

    return "Ok"
from time import sleep
def get_lat_long(country, city):
    sleep(1)
    geolocator = Nominatim(user_agent='wiki_pipeline_fayoded@gmail.com')
    try:
        location = geolocator.geocode(f'{city}, {country}', timeout=10)
        return (location.latitude, location.longitude) if location else None
    except Exception as e:
        print(f"Geocoding error for {city}, {country}: {e}")
        return None


def transform_wikipedia_data(**kwargs):
    data = kwargs['ti'].xcom_pull(key='rows', task_ids='extract_wikipedia_data')

    data =json.loads(data)

    stadium_df =pd.DataFrame(data)

    stadium_df['Location'] = stadium_df.apply(lambda x: get_lat_long(x['Country'], x['Stadium']), axis=1)

    stadium_df['Images'] = stadium_df['Images'].apply(lambda x:x if x not in ['No Image available', '', None] else 'No image available')

    stadium_df['Seating capacity'] = stadium_df['Seating capacity'].str.replace(',', '').astype(int)

    # handle duplicates

    duplicates = stadium_df[stadium_df.duplicated(['Location'])]
    duplicates['Location'] = duplicates.apply(lambda x: get_lat_long(x['Country'], x['City']), axis=1)
    stadium_df.update(duplicates)

    # push back to xcom 
    kwargs['ti'].xcom_push(key='rows', value=stadium_df.to_json())

    return 'OK'

def write_wikipedia_data(**kwargs):
    data =kwargs['ti'].xcom_pull(key='rows', task_ids='transform_wikipedia_data')

    if not data:
        raise ValueError("No data received from XCom")
    data = json.loads(data)
    data = pd.DataFrame(data)
    os.makedirs('data', exist_ok=True)
    file_name = f"stadium_cleaned_{datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}.csv"
    data.to_csv(f'data/{file_name}', index=False)
    return 'OK'