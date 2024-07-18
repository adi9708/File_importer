import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def extract_time_voltage(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Define possible column names
    time_columns = ['Time [s]', 'Datetime', 'DPt Time']
    voltage_columns = ['Voltage [V]', 'Voltage', 'Volts']
    
    # Find the actual column names in the dataframe
    time_col = next((col for col in time_columns if col in df.columns), None)
    voltage_col = next((col for col in voltage_columns if col in df.columns), None)
    
    if 'Date' in df.columns and 'Time' in df.columns:
        df['Date'] = df['Date'].astype(str)
        df['Time'] = df['Time'].astype(str)
        df['Datetime'] = df['Date'] + ' ' + df['Time']
        df['Datetime'] = pd.to_datetime(df['Datetime'], errors='coerce')
        if df['Datetime'].isnull().any():
            print("Failed to parse some datetime values. Here are the first few problematic values:")
            print(df['Datetime'][df['Datetime'].isnull()].head())
        time_list = df['Datetime'].tolist()
        voltage_list = df[voltage_col].tolist()
    else:
        if time_col and voltage_col:
            if time_col == 'DPt Time':
                df['Datetime'] = pd.to_datetime(df[time_col], errors='coerce')
                time_list = df['Datetime'].tolist()
            else:
                time_list = df[time_col].tolist()
            voltage_list = df[voltage_col].tolist()
        else:
            print(f"Time or Voltage columns not found in {file_path}")
            return [], []

    # Ensure all voltage values are numeric
    df['Voltage'] = pd.to_numeric(df[voltage_col], errors='coerce')
    df = df.dropna(subset=['Voltage'])
    df['Voltage'] = df['Voltage'].round(4)  # Adjust the precision to 4 decimal places

    return df['Datetime'].tolist(), df['Voltage'].tolist()



def plot_voltage_traces_from_final_results(output_path):
    plt.figure()
    all_time_data = []
    all_voltage_data = []
    
    for root, dirs, files in os.walk('results'):
        for file in files:
            if file.endswith("_data.csv"):
                file_path = os.path.join(root, file)
                time_list, voltage_list = extract_time_voltage(file_path)
                all_time_data.extend(time_list)
                all_voltage_data.extend(voltage_list)

    # Convert to DataFrame
    df = pd.DataFrame({'Timestamp': all_time_data, 'Voltage': all_voltage_data})
    
    if 'Timestamp' in df.columns and 'Voltage' in df.columns:
        # Split the DataFrame by date
        df['Date'] = pd.to_datetime(df['Timestamp']).dt.date
        df['Time'] = pd.to_datetime(df['Timestamp']).dt.strftime('%H:%M:%S')

        # Sample data for specific dates
        df_2000_02_02 = df[df['Date'] == datetime(2000, 2, 2).date()]
        df_2018_05_02 = df[df['Date'] == datetime(2018, 5, 2).date()]

        # Take a maximum of 20 points from 2000-02-02 and 1-2 points from 2018-05-02
        sample_2000_02_02 = df_2000_02_02.sample(n=min(20, len(df_2000_02_02)), random_state=1)
        sample_2018_05_02 = df_2018_05_02.sample(n=min(2, len(df_2018_05_02)), random_state=1)

        # Combine the sampled data
        df_sampled = pd.concat([sample_2000_02_02, sample_2018_05_02]).sort_index()

        fig, ax = plt.subplots()
        
        df_sampled['Timestamp_str'] = df_sampled['Timestamp'].astype(str)
        ax.plot(df_sampled['Timestamp_str'], df_sampled['Voltage'], marker='o', label='Voltage over Time')
        for i, txt in df_sampled.iterrows():
            ax.annotate(f"{txt['Voltage']}", (txt['Timestamp_str'], txt['Voltage']), fontsize=8, rotation=45)
        
        plt.xlabel('Timestamp')
        plt.ylabel('Voltage [V]')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
