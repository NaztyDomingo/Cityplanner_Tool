import pandas as pd

def order_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    list_with_columns = ['Year',
                        'Region',
                        'Population',
                        'Waste and Sewage',
                        'Machinery',
                        'Electricity and District Heating',
                        'Other heating',
                        'Agriculture',
                        'Transportation',
                        'Industry',
                        'Total Emissions']
    return df[list_with_columns]