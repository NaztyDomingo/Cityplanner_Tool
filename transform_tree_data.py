import filehandler_helper as fh
import xlsx_to_csv_converter as convert
import pandas as pd
import os

def main() -> None:
    # Convert tree_info.xlsx to tree_info.csv
    convert.convert_single_file(fh.get_path_of_folder('tree_data'), fh.get_path_of_folder('transformed_tree_data'), 'tree_info')

    # Get tree averages for CO2 consumption and save that in clean file
    filepath_og = fh.get_path_of_folder('tree_data')
    filepath_of_file_og = os.path.join(filepath_og, 'tree_species_carbon_storing.csv')
    co2_df = pd.read_csv(filepath_of_file_og)

    averages = co2_df.mean()
    avg_df = pd.DataFrame(averages, columns=["avg_co2_consumption"])
    avg_df.drop(['years', 'all_tree_species'], axis=0, inplace=True)
    
    filepath_transformed = fh.get_path_of_folder('transformed_tree_data')
    filepath_of_file_avg = os.path.join(filepath_transformed, 'avg_co2_consumption.csv')
    avg_df.to_csv(filepath_of_file_avg, header=False)

    # Add average co2 consumption data into tree data and save as final_tree_info.csv
    filepath_of_file_tree = os.path.join(filepath_transformed, 'tree_info.csv')
    tree_df = pd.read_csv(filepath_of_file_tree)

    AVGS = ['746.540244', '300.573171', '989.442683', '443.270610', '424.915610', '412.949146', '353.181585']
    tree_df.insert(4, "Average_co2_consumption", AVGS)

    filepath_of_file_final = os.path.join(filepath_transformed, 'final_tree_info.csv')
    tree_df.to_csv(filepath_of_file_final)

if __name__ == "__main__":
    main()