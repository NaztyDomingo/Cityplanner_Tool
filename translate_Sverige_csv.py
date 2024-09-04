import translate_replace as tr
import pandas as pd

file_path = 'data/transformed_sweden_data/sverige.csv'

data = pd.read_csv(file_path)

data = tr.translate_replace(data)

