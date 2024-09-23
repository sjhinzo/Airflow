from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import csv
import os
import requests
import json
import tarfile

# Define the path for the input and output files
source_url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Final%20Assignment/tolldata.tgz'
destination_path = '/opt/airflow/dags/staging'

# Ensure the destination directory exists
os.makedirs(destination_path, exist_ok=True)

# Function to download the dataset
def download_dataset():
    response = requests.get(source_url, stream=True)
    if response.status_code == 200:
        file_path = os.path.join(destination_path, 'toll_data.tgz')
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"File downloaded successfully to {file_path}")
    else:
        print("Failed to download the file")

# Function to extract the downloaded tar.gz file
def extract_tgz():
    file_path = os.path.join(destination_path, 'toll_data.tgz')
    if tarfile.is_tarfile(file_path):
        with tarfile.open(file_path, 'r:gz') as tar:
            tar.extractall(path=destination_path)
        print(f"File extracted successfully to {destination_path}")
    else:
        print(f"{file_path} is not a valid tar.gz file")

# Function to extract data from CSV
def extract_data_from_csv():
    input_file = os.path.join(destination_path, 'vehicle-data.csv')
    output_file = os.path.join(destination_path, 'csv_data.csv')
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        writer.writerow(['Rowid', 'Timestamp', 'Anonymized Vehicle number', 'Vehicle type'])
        next(reader)  # Skip header
        for row in reader:
            writer.writerow(row[:4])
    print(f"CSV data extracted to {output_file}")

# Function to extract data from fixed width file
def extract_data_from_fixed_width():
    input_file = os.path.join(destination_path, 'payment-data.txt')
    output_file = os.path.join(destination_path, 'fixed_width_data.csv')
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Type of Payment code', 'Vehicle Code'])
        for line in infile:
            writer.writerow([line[0:6].strip(), line[6:12].strip()])
    print(f"Fixed-width data extracted to {output_file}")

# Function to consolidate data
def consolidate_data():
    csv_file = os.path.join(destination_path, 'csv_data.csv')
    fixed_width_file = os.path.join(destination_path, 'fixed_width_data.csv')
    output_file = os.path.join(destination_path, 'extracted_data.csv')

    with open(csv_file, 'r') as csv_in, open(fixed_width_file, 'r') as fixed_in, open(output_file, 'w', newline='') as out_file:
        csv_reader = csv.reader(csv_in)
        fixed_reader = csv.reader(fixed_in)
        writer = csv.writer(out_file)
        writer.writerow(['Rowid', 'Timestamp', 'Anonymized Vehicle number', 'Vehicle type', 'Type of Payment code', 'Vehicle Code'])
        next(csv_reader)
        next(fixed_reader)

        for csv_row, fixed_row in zip(csv_reader, fixed_reader):
            writer.writerow(csv_row + fixed_row)
    print(f"Data consolidated into {output_file}")

# Function to transform data
def transform_data():
    input_file = os.path.join(destination_path, 'extracted_data.csv')
    output_file = os.path.join(destination_path, 'transformed_data.csv')

    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        headers = next(reader)  # Read the header
        writer.writerow(headers)  # Write the header to the output file

        vehicle_type_index = headers.index('Vehicle type')  # Find the index of 'Vehicle type'

        # Process and transform rows
        for row in reader:
            row[vehicle_type_index] = row[vehicle_type_index].upper()
            writer.writerow(row)
    print(f"Data transformed and saved to {output_file}")

# Function to export data to JSON
def export_to_json():
    csv_file = os.path.join(destination_path, 'transformed_data.csv')
    json_file = os.path.join(destination_path, 'transformed_data.json')

    data = []
    with open(csv_file, 'r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            data.append(row)

    with open(json_file, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    print(f"Data exported to JSON format in {json_file}")

# Function to check if data files exist
def check_data_files():
    expected_files = [
        os.path.join(destination_path, 'toll_data.tgz'),
        os.path.join(destination_path, 'vehicle-data.csv'),
        os.path.join(destination_path, 'payment-data.txt'),
        os.path.join(destination_path, 'transformed_data.csv'),
        os.path.join(destination_path, 'transformed_data.json')
    ]

    for file in expected_files:
        if not os.path.exists(file):
            raise FileNotFoundError(f"Expected file {file} does not exist.")
    print("All expected data files are present.")

# Function to check if data rows exist
def check_data_rows():
    input_file = os.path.join(destination_path, 'transformed_data.csv')

    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        row_count = sum(1 for _ in reader) - 1  # Subtract 1 for the header row

    if row_count == 0:
        raise ValueError("No data rows found in the transformed data file.")

    print(f"Transformed data file contains {row_count} rows of data.")

# Function to load data (placeholder for your loading logic)
def loading_data():
    # Implement the loading logic here
    print("Data loading logic goes here")

# Default arguments for the DAG
default_args = {
    'owner': 'Bui Tien Sang',
    'start_date': days_ago(0),
    'email': ['buitiensang191@gmail.com'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'ETL_apache_airflow',
    default_args=default_args,
    description='Apache Airflow Final Assignment',
    schedule_interval=timedelta(days=1),
)

# Define the tasks
download_task = PythonOperator(
    task_id='download_dataset',
    python_callable=download_dataset,
    dag=dag,
)

extract_tgz_task = PythonOperator(
    task_id='extract_tgz',
    python_callable=extract_tgz,
    dag=dag,
)

extract_csv_task = PythonOperator(
    task_id='extract_data_from_csv',
    python_callable=extract_data_from_csv,
    dag=dag,
)

extract_fixed_width_task = PythonOperator(
    task_id='extract_data_from_fixed_width',
    python_callable=extract_data_from_fixed_width,
    dag=dag,
)

consolidate_task = PythonOperator(
    task_id='consolidate_data',
    python_callable=consolidate_data,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag,
)

export_json_task = PythonOperator(
    task_id='export_to_json',
    python_callable=export_to_json,
    dag=dag,
)

check_files_task = PythonOperator(
    task_id='check_data_files',
    python_callable=check_data_files,
    dag=dag,
)

check_rows_task = PythonOperator(
    task_id='check_data_rows',
    python_callable=check_data_rows,
    dag=dag,
)

loading_task = PythonOperator(
    task_id='loading_data',
    python_callable=loading_data,
    dag=dag,
)

# Define the task dependencies
download_task >> extract_tgz_task >> [extract_csv_task, extract_fixed_width_task] >> consolidate_task >> transform_task >> check_rows_task >> [loading_task, export_json_task] >> check_files_task