from airflow import DAG
from datetime import datetime 
from airflow.operators.python import PythonOperator

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipelines.wiki_pipeline import extract_wikipedia_data, transform_wikipedia_data, write_wikipedia_data

dag = DAG(
    dag_id="wikiFlow",
    default_args={
        "owner": "Dunsin Fayode",
        "start_date": datetime.now(), 
        "retries": 2
    },
    schedule_interval=None,
    catchup=False
)

# extraction
extract_wikipedia_data = PythonOperator(
    task_id="extract_wikipedia_data",
    python_callable=extract_wikipedia_data,
    provide_context=True,
    op_kwargs={
        "url": "https://en.wikipedia.org/wiki/List_of_association_football_stadiums_by_capacity",
        "headers": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"}
    },
    dag=dag
)
# prep (optional second task if re-enabled)
transform_wikipedia_data = PythonOperator(
    task_id="transform_wikipedia_data",
    python_callable=transform_wikipedia_data,
    provide_context=True,
    dag=dag
)

# write to csv the location

write_wikipedia_data = PythonOperator(
    task_id='write_wikipedia_data',
    provide_context=True,
    python_callable=write_wikipedia_data,
    dag=dag
)

extract_wikipedia_data >> transform_wikipedia_data >> write_wikipedia_data