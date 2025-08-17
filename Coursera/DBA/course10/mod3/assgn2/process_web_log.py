# Creating a DAG

from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import timedelta
from airflow.utils.dates import days_ago


default_args = {
    'owner': 'airflow',
    'start_date': days_ago(0),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='process_web_log',
    default_args=default_args,
    description='ETL process for web_logs',
    schedule_interval=timedelta(days=1),
    catchup=False
) as dag:

    # Task 1: Extract IP-Address
    extract = BashOperator(
        task_id='extract_data',
        bash_command='awk -F " " \'{print $1}\' /home/project/airflow/dags/capstone/accesslog.txt > extracted_data.txt',
        dag=dag
    )

    # Task 2: Remove IP-Address: 198.46.149.143” from text file
    transform = BashOperator(
        task_id='transform_data',
        bash_command='grep -v "198.46.149.143" extracted_data.txt > transformed_data.txt',
        dag=dag
    )

    # Task 3: Archive (tar) the transformed_data.txt file
    load = BashOperator(
        task_id='load_data',
        bash_command='tar -cvf transformed_data.tar transformed_data.txt',
        dag=dag
    )

    # Setting up dependencies
    extract >> transform >> load