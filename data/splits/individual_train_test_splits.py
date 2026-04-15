import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold

import pandas as pd

# Set random
random_state = 42
np.random.seed(random_state)

output_path = 'data/splits/individuals_train_test_splits/'

data  = pd.read_csv(
            'data/splits/updated_annotations.csv',
            dtype = {'tokens': str,'new_tokens': str}
        )
data = data.reset_index(drop=True)





#%% 20% test


y = data['class']
X = data.iloc[:,:-1]

all_individuals = X.new_tokens.drop_duplicates()
y_all_idividuals = y[all_individuals.index]

X_train, X_test, y_train, y_test = train_test_split(
    all_individuals,
    y_all_idividuals, 
    test_size=0.2, 
    random_state=random_state, 
    stratify=y_all_idividuals
)


train = data[data.new_tokens.isin(X_train)]
train.to_csv(os.path.join(output_path, "train.csv"))
test  = data[data.new_tokens.isin(X_test)]
test.to_csv(os.path.join(output_path, "test.csv"))

#%% holdout
y = train['class']
X = train.iloc[:,:-1]

all_individuals = X.new_tokens.drop_duplicates()
y_all_idividuals = y[all_individuals.index]

X_train, X_test, y_train, y_test = train_test_split(
    all_individuals,
    y_all_idividuals, 
    test_size=0.2, 
    random_state=random_state, 
    stratify=y_all_idividuals
)


holdout_train = data[data.new_tokens.isin(X_train)]
holdout_train.to_csv(os.path.join(output_path, 'holdout_train.csv'))
holdout_val  = data[data.new_tokens.isin(X_test)]
holdout_val.to_csv(os.path.join(output_path, 'holdout_val.csv'))

#%% cv

y = train['class']
X = train.iloc[:,:-1]

all_individuals = X.new_tokens.drop_duplicates()
y_all_idividuals = y[all_individuals.index]


### Stratified KFold
skf = StratifiedKFold(n_splits=5,shuffle=True)
splits = skf.split(all_individuals,y_all_idividuals)
for idx,(indices_train,indices_val) in enumerate(splits):
    
    X_train = all_individuals.values[indices_train]
    train = data[data.new_tokens.isin(X_train)]
    train.to_csv(os.path.join(output_path, f'SKF_TRAIN_Fold_{idx+1}.csv'))
    
    X_test = all_individuals.values[indices_val]
    test  = data[data.new_tokens.isin(X_test)]
    test.to_csv(os.path.join(output_path, f'SKF_VAL_Fold_{idx+1}.csv'))
   
# %%
