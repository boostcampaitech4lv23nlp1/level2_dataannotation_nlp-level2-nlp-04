from ast import literal_eval
import pandas as pd

train = pd.read_csv('train.csv')
dev = pd.read_csv('dev.csv')
test = pd.read_csv('test.csv')

def making_dict(df):
    df['subj_index'] = df['subj_index'].apply(lambda x: literal_eval(x))
    df['obj_index'] = df['obj_index'].apply(lambda x: literal_eval(x))

    df['subject_entity'] = None
    df['object_entity'] = None
    
    x = dict()
    y = dict()
    for i in df.index:
        x['word'] = df['subj_entity'][i]
        x['start_idx'] = df['subj_index'][i]['start_idx']
        x['end_idx'] = df['subj_index'][i]['end_idx']
        x['type'] = df['subj_type'][i]
        df['subject_entity'][i] = x
        
        y['word'] = df['obj_entity'][i]
        y['start_idx'] = df['obj_index'][i]['start_idx']
        y['end_idx'] = df['obj_index'][i]['end_idx']
        y['type'] = df['obj_type'][i]
        df['object_entity'][i] = y
        
making_dict(train)
making_dict(dev)
making_dict(test)

# save
train.to_csv('train_fix_form.csv')
dev.to_csv('dev_fix_form.csv')
test.to_csv('test_fix_form.csv')