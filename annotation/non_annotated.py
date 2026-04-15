import os
import pandas as pd





df = pd.read_csv(('/home/vitorpmatias/Documentos/MESTRADO/TESE/TESE/'
                 'paper_benchmark/data_manipulation/all_data_available.csv'),
                 index_col=0,dtype = {'tokens': str,'new_tokens': str})



path = '/home/vitorpmatias/Documentos/MESTRADO/TESE/TESE/annotation/users'

users_dirs = os.listdir(path)
annotated = []
for user in users_dirs:
    user_files_path = path + '/' + user

    user_files  = os.listdir(user_files_path)
    for file in user_files:
        if file.startswith('sessao'):
            csv_path = user_files_path + '/' + file
            annotated.append(pd.read_csv(csv_path,
                                         index_col=0,
                                         dtype = {
                                             'tokens': str,
                                             'new_tokens': str
                                             }))


annotated.append(
    pd.read_csv(
        ('/home/vitorpmatias/Documentos/MESTRADO/TESE/TESE/annotation/'
        'separated_datasets_for_annotators/rotulacao_joao/all_data.csv'),
        index_col=0,dtype = {'tokens': str,'new_tokens': str})
)

annotated.append(
    pd.read_csv(
        ('/home/vitorpmatias/Documentos/MESTRADO/TESE/TESE/annotation/'
         'separated_datasets_for_annotators/rotulacao_rodrigo/all_data.csv'),
        index_col=0,dtype = {'tokens': str,'new_tokens': str})
)




df_annotated = pd.concat(annotated)

df_non_annotated = df[~df['new_tokens'].isin(df_annotated['new_tokens'].values)]

df_non_annotated = df_non_annotated.sort_values(by=['number_of_photos'],
                                                ascending=False)
df_non_annotated.reset_index(drop=True)

df_non_annotated.to_csv(('/home/vitorpmatias/Documentos/MESTRADO/TESE/TESE/'
                         'annotation/non_annotated.csv'))
