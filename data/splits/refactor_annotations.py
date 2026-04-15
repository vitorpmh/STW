import pandas as pd


df = pd.read_csv('data/splits/all_annotated_data.csv')


condition = (df['dataset'] == 'Casia Face Africa') & (df['paths'].str.contains('C2'))

df.loc[condition, 'new_tokens'] = df['tokens'].astype(str) + "_C2_" + df['dataset']

condition = (df['dataset'] == 'Casia Face Africa') & (df['paths'].str.contains('C1'))

df.loc[condition, 'new_tokens'] = df['tokens'].astype(str) + "_C1_" + df['dataset']

condition = (df['dataset'] == 'CelebA') & (df['paths'].str.contains('png'))
df.loc[condition, 'paths'] = df.loc[condition, 'paths'].str.replace('.png', '.jpg', regex=False)

condition = (df['dataset'] == 'CelebA') & (df['paths'].str.contains('_png'))
df.loc[condition, 'paths'] = df.loc[condition, 'paths'].str.replace('_png', '', regex=False)

df.to_csv('data/splits/updated_annotations.csv', index=False)

