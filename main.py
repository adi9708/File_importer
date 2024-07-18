import os
from file_transformation import file_type_chooser
from preprocessing import normalize_and_save_all_csv_files
from generate_graphs import plot_voltage_traces_from_final_results

def main():
    file_paths = [
        'test_files/1/1.xyz',
        'test_files/2/2.xyz',
        'test_files/3/3.xyz',
        # 'test_files/4/4.mdb'
    ]

    # Process and save data files
    file_type_chooser(file_paths)

    # Normalize and save all CSV files
    normalize_and_save_all_csv_files('results')

    # Plot voltage traces from final results
    plot_voltage_traces_from_final_results(os.path.join('results', 'voltage_traces_final.png'))

    print("Data processing, normalization, and plotting completed successfully.")

if __name__ == "__main__":
    main()
