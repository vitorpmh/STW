import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
import pandas as pd
# Set random
random_state = 42
np.random.seed(random_state)

output_path = 'data/splits/images_train_test_splits/'


data  = pd.read_csv(
            'data/splits/updated_annotations.csv',
            dtype = {'tokens': str,'new_tokens': str}
        )
data = data.reset_index(drop=True)



#%% 10 person custom test
custom_test_df = pd.DataFrame(columns=data.columns)
for label in range(1,11):
    for i in range(10):
        name = data[data['class'] == label].sort_values(by='number_of_photos').iloc[0]['new_tokens']
        _df = data[data['new_tokens']==name]
        custom_test_df = pd.concat([custom_test_df,_df])
        data = data[data['new_tokens'] != name]

custom_test_df = custom_test_df.reset_index(drop=True)
custom_test_df.to_csv(os.path.join(output_path,'custom_test.csv'))
data = data.reset_index(drop=True)

#%% 20% test


y = data['class']
X = data.iloc[:,:-1]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y, 
    test_size=0.2, 
    random_state=random_state, 
    stratify=y
)


train = data.iloc[X_train.index]
train.to_csv(os.path.join(output_path, "train.csv"))
test  = data.iloc[X_test.index]
test.to_csv(os.path.join(output_path, "test.csv"))

#%% holdout
y = train['class']
X = train.iloc[:,:-1]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y, 
    test_size=0.2, 
    random_state=random_state, 
    stratify=y
)


holdout_train = data.iloc[X_train.index]
holdout_train.to_csv(os.path.join(output_path, 'holdout_train.csv'))
holdout_val  = data.iloc[X_test.index]
holdout_val.to_csv(os.path.join(output_path, 'holdout_val.csv'))

#%% cv

y = train['class']
X = train.iloc[:,:-1]



### Stratified KFold
skf = StratifiedKFold(n_splits=5,shuffle=True)
splits = skf.split(X,y)
for idx,(indices_train,indices_val) in enumerate(splits):
    
    train = data.iloc[indices_train]
    train.to_csv(os.path.join(output_path, f'SKF_TRAIN_Fold_{idx+1}.csv'))
    
    test  = data.iloc[indices_val]
    test.to_csv(os.path.join(output_path, f'SKF_VAL_Fold_{idx+1}.csv'))
   
# %%
