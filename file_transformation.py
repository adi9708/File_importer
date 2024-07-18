import os
import pandas as pd
import subprocess
from datetime import datetime, timedelta

def extract_data_metadata_init(file_path):
    if file_path.endswith("1.xyz"):
        return first_file_extractor(file_path)
    elif file_path.endswith("2.xyz"):
        return second_file_extractor(file_path)
    elif file_path.endswith("3.xyz"):
        return third_file_extractor(file_path)
    else:
        return "Wrong File", None, None

def first_file_extractor(file_path):
    with open(file_path, 'r') as file:
        content = file.readlines()
    metadata_lines = []
    data_lines = []
    data_start_index = 0
    test_start_date = None

    for i, line in enumerate(content):
        # If Time [s] is present in line, assumption is that metadata content ends here
        # and actual data starts from this column header name 
        if 'Time [s]' in line:
            data_start_index = i
            break
        # We need to combine TestStartDate in metadata with actual time (Time (s))
        # given in data to get the original timestamp
        if 'TestStartDate' in line:
            test_start_date = line.split(':')[1].strip().split(',')[0]
        metadata_lines.append(line.strip())

    data_lines = content[data_start_index:]
    
    return metadata_lines, data_lines, test_start_date

def second_file_extractor(file_path):
    with open(file_path, 'r') as file:
        content = file.readlines()
    # Assuming metadata_lines would always be only first line in this type of data
    metadata_lines = content[0]
    data_lines = content[1:]
    return [metadata_lines], data_lines, None

def third_file_extractor(file_path):
    with open(file_path, 'r') as file:
        content = file.readlines()
    metadata = []
    data = []
    data_section = False
    # In all the lines of metadata, there is a pattern:
    # Header name followed by ":;" and then value. Split it into metadata and data
    # wherever this pattern ends
    for line in content:
        stripped_line = line.strip()
        
        if ':;' in stripped_line:
            metadata.append(stripped_line)
        elif ';' in stripped_line:
            data.append(stripped_line.replace(';', ',') + '\n')
    return metadata, data, None

def read_mdb_file(file_path, output_dir):
    # Use mdb-tools to get table names
    tables = subprocess.check_output(['mdb-tables', '-1', file_path]).decode().strip().split('\n')
    os.makedirs(output_dir, exist_ok=True)

    data_frames = {}
    for table in tables:
        if table:
            csv_path = os.path.join(output_dir, f"{table}.csv")
            with open(csv_path, 'w') as f:
                subprocess.run(['mdb-export', file_path, table], stdout=f)
            data_frames[table] = pd.read_csv(csv_path)
   
    return data_frames

def write_data(metadata, data, file_path):
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    result_dir = os.path.dirname(file_path).replace('test_files', 'results')
    os.makedirs(result_dir, exist_ok=True)
    metadata_file_path = os.path.join(result_dir, f'{base_name}_metadata.txt')
    data_file_path = os.path.join(result_dir, f'{base_name}_data.csv')

    with open(metadata_file_path, 'w') as metadata_file:
        metadata_file.write("\n".join(metadata))

    with open(data_file_path, 'w') as data_file:
        data_file.writelines(data)


def save_data_to_csv(data, output_path):
    data.to_csv(output_path, index=False)

def add_test_start_date_to_time(file_path, test_start_date):
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Convert TestStartDate to datetime
    start_datetime = datetime.strptime(test_start_date, "%Y-%m-%d")
    
    # Add TestStartDate to Time [s] column
    df['Datetime'] = df['Time [s]'].apply(lambda x: start_datetime + timedelta(seconds=float(x)))
    df['Datetime'] = df['Datetime'].astype(str)
    df.to_csv(file_path, index=False)


def file_type_chooser(file_paths):
    for file_path in file_paths:
        result_dir = os.path.dirname(file_path).replace('test_files', 'results')
        if file_path.endswith('.xyz'):
            metadata, data, test_start_date = extract_data_metadata_init(file_path)
            write_data(metadata, data, file_path.replace('test_files', 'results'))
            # Combining timestamp values for first file
            if file_path.endswith("1.xyz"):
                add_test_start_date_to_time(os.path.join(result_dir, '1_data.csv'), test_start_date)
        elif file_path.endswith('.mdb'):
            mdb_data = read_mdb_file(file_path, result_dir)
            for table_name, df in mdb_data.items():
                save_data_to_csv(df, os.path.join(result_dir, f'{table_name}.csv'))
