

from airflow import DAG
from datetime import datetime 
from airflow.operators import PythonOperator

import os
import sys

sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipelines.wiki_pipeline import get_wikipedia_page

dag =DAG(
    dag_id ="wikiFlow",
    default_args={
        "owner": "Dunsin Fayode",
        "start_date": datetime(2025,09,10),
    },
    schedule_interval=None,
    catchup=False
)

# extraction
extract_data_from_wikipedia = PythonOperator(
    task_id="extract_data_from_wikipedia",
    python_callable=get_wikipedia_page,
    provide_context=True,
    op_kwargs={"url": "https://en.wikipedia.org/wiki/List_of_association_football_stadiums_by_capacity", 
               "headers": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"}},
    dag=dag

)

# prep