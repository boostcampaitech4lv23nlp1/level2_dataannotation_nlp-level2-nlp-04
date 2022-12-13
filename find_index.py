import re
import pandas as pd




def find_entity(sentence):
    '''
    input
        sentence : sentence with entity marking (* : subj entity   & : obj entity)

        
    output
        sentence : origin sentence
        subj : subj_entity
        obj : obj_entity
        subj_dict : {'start_idx': , 'end_idx': }
        obj_dict : {'start_idx': , 'end_idx': }
    
    example
        &독일&의 *게오르그 하클*은 이번 대회 루지 싱글 종목에서 은메달을 획득함으로써, 개인종목에서 올림픽 대회 5연속 메달 획득에 성공한 최초의 선수가 되었다.

        
        sentence : 독일의 게오르그 하클은 이번 대회 루지 싱글 종목에서 은메달을 획득함으로써, 개인종목에서 올림픽 대회 5연속 메달 획득에 성공한 최초의 선수가 되었다.
        subj : 게오르그 하클
        obj : 독일
        subj_dict : {'start_idx': 4, 'end_idx': 11}
        obj_dict : {'start_idx': 0, 'end_idx': 2}
        
    '''
    m_subj=re.search(r"\*[^\*]+\*",sentence)
    m_obj=re.search(r"&[^&]+&",sentence)
    subj_with_marker = sentence[m_subj.start():m_subj.end()]
    obj_with_marker = sentence[m_obj.start():m_obj.end()]
    
    subj = subj_with_marker[1:-1]
    obj = obj_with_marker[1:-1]

    subj_with_marker = re.sub(r'\*','\*',subj_with_marker)
    
    subj_dict= dict()
    obj_dict = dict()

    
    if m_subj.start()<m_obj.start():

        m_subj = re.search(subj_with_marker,sentence)
        subj_dict["start_idx"] = m_subj.start()
        subj_dict["end_idx"] = m_subj.start() + len(subj)
        sentence = re.sub(subj_with_marker,subj,sentence)

        m_obj = re.search(obj_with_marker,sentence)
        obj_dict["start_idx"] = m_obj.start()
        obj_dict["end_idx"] = m_obj.start() + len(obj)
        sentence = re.sub(obj_with_marker,obj,sentence)

    else:
        m_obj = re.search(obj_with_marker, sentence)
        obj_dict["start_idx"] = m_obj.start()
        obj_dict["end_idx"] = m_obj.start() + len(obj)
        sentence = re.sub(obj_with_marker,obj,sentence)

        m_subj = re.search(subj_with_marker,sentence)
        subj_dict["start_idx"] = m_subj.start()
        subj_dict["end_idx"] = m_subj.start() + len(subj)
        sentence = re.sub(subj_with_marker,subj,sentence)
        
    return sentence, subj, obj, subj_dict, obj_dict


if __name__ == '__main__':
    
    input_df = pd.read_csv('./temp.csv', encoding='utf8')
    
    subj_list = []
    obj_list = []
    subj_type_list = input_df['subj_type']
    obj_type_list = input_df['obj_type']

    sentence_list = []
    subj_dict_list = []
    obj_dict_list = []

    for sentence in input_df["sentence"]:
        sentence_, subj_, obj_, subj_dict_, obj_dict_ = find_entity(sentence)
        sentence_list.append(sentence_)
        subj_list.append(subj_)
        obj_list.append(obj_)
        subj_dict_list.append(subj_dict_)
        obj_dict_list.append(obj_dict_)
        
    output_df = pd.DataFrame({'id':range(len(sentence_list)),'sentence':sentence_list,'subj_entity':subj_list,'obj_entity':obj_list,'subj_type':subj_type_list,'obj_type':obj_type_list, 'subj_index':subj_dict_list,'obj_index':obj_dict_list })

    output_df.to_csv('append.csv')
        