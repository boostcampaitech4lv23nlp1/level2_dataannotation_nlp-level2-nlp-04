## ./outputs 폴더에 {workername}.csv 파일을 넣고 실행

import pandas as pd
import os


def merge(folder_dir):
    """디렉토리에 있는 모든 csv파일을 행기준으로 합침

    Args:
        folder_dir (str): 합치고자 하는 파일이 있는 폴더의 디렉토리
            column: [id,sentence,subj_entity,obj_entity,subj_type,obj_type,subj_index,obj_index,relation]
    
    Returns:
        all_df (pandas.Dataframe): 합쳐진 데이터프레임
            column: [wkr-idx,sentence,subj_entity,obj_entity,subj_type,obj_type,subj_index,obj_index,relation]
    """

    file_name_list = os.listdir(folder_dir)
    file_df_list = []

    for file_name in file_name_list:
        file_df = pd.read_csv(folder_dir + "/" + file_name)

        file_df['id'] = file_df['id'].apply(lambda x: file_name.split('.')[0] + "-" + str(x))

        file_df_list.append(file_df)
    
    all_df = pd.concat(file_df_list)

    return all_df





def drop_duplicates(all_df):
    """인자로 주어진 데이터프레임의 문장, subject entity, object entity가 모두 겹치면 drop시킴

    Args:
        all_df (pandas.DataFrame): 데이터가 들어있는 데이터프레임

    Returns:
        pandas.DataFrame: 중복제거된 데이터가 들어있는 데이터프레임
    """
    
    dropped_df = all_df.drop_duplicates(subset=["sentence","subj_entity","obj_entity"])

    print("=" * 10)
    print('num of dropped row:', len(all_df) - len(dropped_df))
    print("=" * 10)

    return dropped_df


if __name__ == '__main__':
    all_df = merge('./outputs')
    dropped_df = drop_duplicates(all_df)

    dropped_df.to_csv('final_dataset_for_tagging.csv', index=False)