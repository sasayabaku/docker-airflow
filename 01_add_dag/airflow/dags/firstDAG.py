"""
First DAG Python file
"""

from datetime import timedelta
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator
from pprint import pprint
from airflow.operators.python import PythonOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2)
}

dag = DAG(
    'first_test',
    default_args=default_args,
    description="For test execute DAG",
    schedule_interval=timedelta(days=1),
    catchup=False
)

t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag
)

t2 = BashOperator(
    task_id='sleep',
    depends_on_past=False,
    bash_command='sleep 5',
    retries=3,
    dag=dag
)

def print_context(ds, **kwargs):
    pprint(kwargs)
    print(ds)
    return 'Hello! Airflow!!!'

run_this = PythonOperator(
    task_id='print_the_context',
    provide_context=True,
    python_callable=print_context,
    dag=dag
)

t1 >> t2 >> run_this