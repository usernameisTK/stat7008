import pandas as pd

def get_topic_by_filename(fn):
    file_path='Report_Topics.xlsx'
    df = pd.read_excel(file_path)

    matching_row = df[df['File Name'] == fn]

    if not matching_row.empty:
        return matching_row['Topic'].values[0]
    else:
        return "No matching topic found."
    
    
