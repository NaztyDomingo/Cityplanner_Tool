def transform_data(data):
    print(f"Columns available in transform_data: {data.columns.tolist()}")

    try:
        data['Total Emissions'] = data.iloc[1:].sum(axis=1)
    except KeyError as e:
        print(f"Column error: {e}")
        raise

    
    print(data)

