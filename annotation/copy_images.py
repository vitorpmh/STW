import copy
import os
import shutil
import pandas as pd
from tqdm import tqdm
csv_file = "/home/vitorpmatias/Documentos/MESTRADO/TESE/TESE/annotation/data_to_annotate_joao_marcus.csv"
output_folder = "separated_datasets_for_annotators/rotulacao_joao_marcus/test"

os.makedirs(output_folder, exist_ok=True)

path_list = []
df = pd.read_csv(csv_file,index_col=0)

for index, row in tqdm(df[~df.duplicated(subset=['new_tokens'], keep='first')].sort_values(by='new_tokens').iterrows(),total = 999):
    tokens,dataset,new_tokens,number_of_photos, label = row[1:]

    individual_df = df[df['new_tokens'] == row['new_tokens']]
    ext_list = individual_df['paths'].apply(os.path.splitext).str[-1].to_list()
    source_path_list  = individual_df['paths'].to_list()
    for i,(source_path,ext) in enumerate(zip(source_path_list,ext_list)):
        destination_path = 'images/' + row['new_tokens'] + f'_{i:05d}' + ext
        
        path_list.append([
            destination_path,
            tokens,
            dataset,
            new_tokens,
            number_of_photos,
            label
            ])
    
        if os.path.exists(source_path):
            try:
                shutil.copy(source_path, 'separated_datasets_for_annotators/rotulacao_joao_marcus/' + destination_path)
            except Exception as e:
                print(f"Error copying {source_path}: {e}")
        else:
            print(f"Source file not found: {source_path}")


new_df = pd.DataFrame(path_list,colums = df.columns)

new_df = new_df.sort_values(by=['dataset','paths'])
new_df = new_df.reset_index(drop=True)
new_df.to_csv('marcus_joao_data.csv')

print("File copying completed.")
