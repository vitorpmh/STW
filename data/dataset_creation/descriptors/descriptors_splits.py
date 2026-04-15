import os
import pandas as pd

main_path = '/store/vitorpmatias/TESE/TESE/'

segmentation = ['cheeks_nose','skin_only',]
annotations = ['cheeks_nose_only','face_only',]
path_ = ['paths_cheeks_nose','paths_face_only',]
for seg,an,paths_seg in zip(segmentation,annotations,path_):
    annotation = os.path.join(
        main_path,
        'dissertation/dataset',
        f'anotations_{an}.csv')
    annotation_df = pd.read_csv(annotation)
    for bins in [8,16,32,64,128]:
        descriptors_df = ('/store/vitorpmatias/TESE/TESE/dissertation'
                          f'/CCVmodel/descriptors/descriptors_{seg}_{bins}.csv')
        descriptors_df = pd.read_csv(descriptors_df)        

        splits = ['individuals','images']

        for split in splits:
                        
            splits_folder_path = ('dissertation/dataset'
                                  f'/{split}_train_test_splits')
            split_new_folder = os.path.join(
                main_path,
                f'dissertation/CCVmodel/descriptors/{split}_train_test_splits')
            

            csv_paths = os.listdir(f'{main_path}{splits_folder_path}')    

            for csv in csv_paths:
                # if csv != 'custom_test.csv':
                #     continue
                # else:
                split_df = os.path.join(main_path,splits_folder_path,csv)
                split_df = pd.read_csv(split_df,index_col=0)
                split_df[paths_seg] = annotation_df[
                    annotation_df.paths.isin(
                        split_df.paths)][paths_seg].values
                split_decriptors_df = descriptors_df[
                    descriptors_df.paths.isin(split_df[paths_seg])]
                save_path = os.path.join(
                    main_path,split_new_folder,str(bins))
                os.makedirs(save_path, exist_ok=True)
                split_decriptors_df.to_csv(
                    save_path + f'/{seg}_{csv}',index=False)