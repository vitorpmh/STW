import os
import pandas as pd
main_path = '/store/vitorpmatias/TESE/TESE/'
datasets_path = os.path.join(main_path,'dissertation/CCVmodel/descriptors')

def bin_columns(df, bin_size):
    new_data = {}
    df_copy = df.copy()

    for prefix in ['gch_hist', 'coherent_64', 'incoherent_64', 'border', 'interior']:  
        cols = [col for col in df.columns if col.startswith(prefix)]  # Select feature group
        df_copy = df_copy.drop(columns = cols)
        num_features = len(cols)  
        step = max(1, num_features // bin_size)  # Ensure at least 1 column per bin

        for i in range(bin_size):  # Create exactly `bin_size` bins
            bin_cols = cols[i * step: (i + 1) * step]  # Select bin columns
            if bin_cols:  # Check for non-empty bin
                new_col_name = f"{prefix}_{i}"  # Rename aggregated column
                new_data[new_col_name] = df[bin_cols].sum(axis=1)  # Sum columns in bin
    return pd.concat([df_copy,pd.DataFrame(new_data)],axis=1)



# os.makedirs(os.path.join(datasets_path,'rebinarized'), exist_ok=True)

# splits = [ 
#     name 
#     for name in os.listdir(datasets_path) 
#     if (os.path.isdir(os.path.join(datasets_path, name)) 
#     and name != '__pycache__' 
#     and name != 'rebinarized'
#     and name != 'old_descriptors')]
# for split in splits:
#     bins_list = os.listdir(os.path.join(datasets_path,split))
#     for bins in bins_list:
#         csvs = os.listdir(os.path.join(datasets_path,split,bins))
#         for csv in csvs:
#             # if 'custom_test' not in csv:
#             #     continue
#             # if os.path.exists(os.path.join(datasets_path,'rebinarized',split,bins,csv)):
#             #     continue
            
#             # else:
#             df_path = os.path.join(datasets_path,split,bins,csv)
#             df = pd.read_csv(df_path)

                
            
#             df_rebinarized = bin_columns(df, int(bins))
#             os.makedirs(os.path.join(datasets_path,'rebinarized',split,bins), exist_ok=True)
#             df_rebinarized.to_csv(os.path.join(datasets_path,'rebinarized',split,bins,csv), index=False)