import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def normalize_and_save_all_csv_files(input_dir):
    csv_files = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".csv"):
                csv_files.append(os.path.join(root, file))
    
    standardized_columns = {
        'time[s]': 'Time(s)',
        'datetime': 'Datetime',
        'dpt_time': 'Time(s)',
        'voltage[v]': 'Voltage(V)',
        'voltage': 'Voltage(V)',
        'volts': 'Voltage(V)'
    }
    
    for file_path in csv_files:
        df = pd.read_csv(file_path)
        
        # Standardize column names
        df.columns = [standardized_columns.get(col.strip().title(), col.strip().title()) for col in df.columns]
        
        # Check if all values in the column are of the same datatype and handle missing values
        # for col in df.columns:
        #     if df[col].dtype == 'object':
        #         try:
        #             df[col] = pd.to_numeric(df[col], errors='coerce')
        #         except ValueError:
        #             df.drop(columns=[col], inplace=True)
        
        # Fill missing values for numerical columns
        df.fillna(0, inplace=True)
        
        # Handle categorical columns with null values
        for col in df.select_dtypes(include=['object']).columns:
            unique_vals = df[col].dropna().unique()
            if len(unique_vals) == 1:
                df[col].fillna(unique_vals[0], inplace=True)
        
        # Normalize float columns to round precision 5
        for col in df.select_dtypes(include=[np.float64]).columns:
            df[col] = df[col].round(5)
        
        # Save the normalized DataFrame to the same directory
        df.to_csv(file_path, index=False)

def add_test_start_date_to_time(file_path, test_start_date):
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Convert TestStartDate to datetime
    start_datetime = datetime.strptime(test_start_date, "%Y-%m-%d")
    
    # Add TestStartDate to Time [s] column
    df['Datetime'] = df['Time [s]'].apply(lambda x: start_datetime + timedelta(seconds=float(x)))
    df['Datetime'] = df['Datetime'].astype(str)
    df.to_csv(file_path, index=False)

def save_data_to_csv(data, output_path):
    data.to_csv(output_path, index=False)
