import xlsx_to_csv_converter as xtcc
import filehandler_helper as fh
import transform as t
import pandas as pd


def main() -> None:
    data1 = _transform_regions()

    data2 = _tranform_cities()

    print('All files transformed...')

    data_to_csv(data1, data2)

def _tranform_cities() -> None:
    # Converting sweden cities file to csv
    xtcc.convert_single_file('sweden_data', 'sweden_data', 'countyreport_CO2')

    filename = 'countyreport_CO2.csv'
    folder = 'sweden_data'
    filepath = fh.get_path_of_file(folder, filename)
    data = pd.read_csv(filepath, index_col=False)
    
    # translating column headers and main section values and replacing special charachters in city, region values.  
    data = t.translate_replace(data)

    #Droping redundant rows before transformation
    data = t.drop_rows_for_cities(data)

    #Dropping redundant columns before transformation
    data = t.drop_columns_for_cities(data)

    #Transforming data
    data1 = t.transform_city_data(data)

    return data1 

def _transform_regions():
    xtcc.convert_single_file('sweden_data', 'sweden_data', 'countyreport_CO2')

    filename = 'countyreport_CO2.csv'
    folder = 'sweden_data'
    filepath = fh.get_path_of_file(folder, filename)
    data = pd.read_csv(filepath, index_col=False)
    
    # translating column headers and main section values and replacing special charachters in city, region values.  
    data = t.translate_replace(data)

    #Droping redundant rows before transformation
    data = t.drop_rows_for_regions(data)

    #Dropping redundant columns before transformation
    data = t.drop_columns_for_regions(data)

    #Transforming data
    data2 = t.transform_region_data(data)

    return data2 

def data_to_csv(data1: pd.DataFrame, data2: pd.DataFrame) -> None:
    #Saving cities
    filename1 = 'sweden_cities_emissions.csv'
    folder1 = 'transformed_sweden_data'
    filepath1 = fh.get_path_of_file(folder1, filename1)
    data1.to_csv(filepath1, index=False)

    #Saving regions
    filename2 = 'sweden_regions_emissions.csv'
    folder2 = 'transformed_sweden_data'
    filepath2 = fh.get_path_of_file(folder2, filename2)
    data2.to_csv(filepath2, index=False)




if __name__ == "__main__":
    main()


