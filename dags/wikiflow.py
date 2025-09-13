from airflow import DAG
from datetime import datetime 
from airflow.operators.python import PythonOperator

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipelines.wiki_pipeline import extract_wikipedia_data

dag = DAG(
    dag_id="wikiFlow",
    default_args={
        "owner": "Dunsin Fayode",
        "start_date": datetime(2025, 9, 13), 
        "retries": 2,
    },
    schedule_interval=None,
    catchup=False
)

# extraction
extract_data_from_wikipedia = PythonOperator(
    task_id="extract_data_from_wikipedia",
    python_callable=extract_wikipedia_data,
    provide_context=True,
    op_kwargs={
        "url": "https://en.wikipedia.org/wiki/List_of_association_football_stadiums_by_capacity",
        "headers": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"}
    },
    dag=dag
)
# prep (optional second task if re-enabled)
# process_wikipedia_data = PythonOperator(
#     task_id="process_wikipedia_data",
#     python_callable=get_wikipedia_data,
#     provide_context=True,
#     op_kwargs={"html": "{{ task_instance.xcom_pull(task_ids='extract_data_from_wikipedia') }}"},
#     dag=dag
# )
#
# extract_data_from_wikipedia >> process_wikipedia_data