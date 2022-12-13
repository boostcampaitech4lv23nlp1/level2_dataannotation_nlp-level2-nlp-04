import json
import glob
import re
import os
import pandas as pd
import requests
import zipfile
import shutil



# 데이터 다운로드
def file_download(id, pw):
    '''
    input
        id: tagtog id
        pw: tagtog pw
    output
        o_file: 다운로드 받은 zip 파일 이름
    '''
    o_file = 'temp.zip'  # zip 파일
    if os.path.exists(o_file):
        os.remove(o_file)

    session = requests.session()
    login_info = {
        "loginid":USER_ID,
        "password":USER_PW
    }

    url_login = "https://www.tagtog.com/-login"
    url_file = "https://www.tagtog.com/yiye/olympics/-downloads/dataset-as-anndoc"

    with requests.Session() as s:
        login_req = s.post(url_login, data=login_info)
        r = s.get(url_file)
        
        with open(o_file,"wb") as output:
            output.write(r.content)
            
    return o_file

## 데이터 추출
def file_extraction(o_file):
    '''
    input
        o_file: 다운로드 받은 zip 파일 이름
    output
        dir_path: zip 파일의 추출한 파일이 있는 경로
    '''
    dir_path = "./extraction/"

    zip_ = zipfile.ZipFile(o_file)
    if os.path.exists(dir_path):  # 만약 존재한다면 모두 삭제
        shutil.rmtree(dir_path)
    zip_.extractall(dir_path)  # extraction 파일 밑에 추출
    
    return dir_path




## 데이터 정제 및 데이터 프레임 구축
def to_entity_csv(dir_path, work_dir):
    '''
    input
        dir_path: ann.json, plain.html 디렉터리가 있는 작업 경로
        work_dir: 실제 json 파일이 있는 마지막 디렉터리 경로
    output
        df: output DataFrame
    '''
    # 경로 설정
    ENTITY_DIR = dir_path + f"ann.json/master/pool/{work_dir}"  #json
    SENTENCE_DIR = dir_path + f"plain.html/pool/{work_dir}"   # html
    
    
    # 범주 가져오기
    annotation_legend_path = dir_path + "annotations-legend.json"
    with open(annotation_legend_path,"r") as f:
        annotation_legend = json.load(f)
    
    subj_entity_set = set()
    obj_entity_set = set()
    
    for i in annotation_legend.keys():
        if annotation_legend[i].split('-')[0] == "SUBJ":
            subj_entity_set.add(i)
        elif annotation_legend[i].split('-')[0] == "OBJ":
            obj_entity_set.add(i)
    
    
    # entity 추출 함수
    def get_entities(relation_json):
        '''
        input
            relation_json: entity json_file
        output
            subj_info: {'word': '', 'start_idx': , 'end_idx': , 'type': ''}
            obj_info: {'word': '', 'start_idx': , 'end_idx': , 'type': ''}
        '''
        subj_entity=None
        obj_entity=None

        is_annotation = True
        try:
            entities1 = relation_json['entities'][0]
            entities2 = relation_json['entities'][1]
            if entities1["classId"] in subj_entity_set and entities2["classId"] not in subj_entity_set:
                subj_entity,obj_entity = entities1,entities2
            elif entities2["classId"] in subj_entity_set and entities1["classId"] not in subj_entity_set:
                obj_entity,subj_entity = entities1,entities2
            else:
                is_annotation = False
        except:
            is_annotation = False

        subj_info = None
        obj_info =None
        if is_annotation:
            subj_info = dict()
            obj_info  = dict()

            subj_info['word'] = subj_entity["offsets"][0]['text']
            subj_info['start_idx'] = subj_entity["offsets"][0]['start']
            subj_info['end_idx'] = subj_info['start_idx'] + len(subj_info['word'])
            subj_info['type'] = annotation_legend[subj_entity["classId"]].split('-')[-1]

            obj_info['word'] = obj_entity["offsets"][0]['text']
            obj_info['start_idx'] = obj_entity["offsets"][0]['start']
            obj_info['end_idx'] = obj_info['start_idx'] + len(obj_info['word'])
            obj_info['type'] = annotation_legend[obj_entity["classId"]].split('-')[-1]

        return subj_info, obj_info
    
    # sentence 추출 함수
    def get_sentence(context_json, parts, subj_info, obj_info):
        '''
        input
            context_json: sentence html file
            subj_info: before processing
                {'word': '', 'start_idx': , 'end_idx': , 'type': ''}
            obj_info: before processing 
                {'word': '', 'start_idx': , 'end_idx': , 'type': ''}
        output

            subj_info: after processing
                {'word': '', 'start_idx': , 'end_idx': , 'type': ''}
            obj_info: after processing 
                {'word': '', 'start_idx': , 'end_idx': , 'type': ''}
        '''
        subj_marker = '#SUBJ#'
        obj_marker = '#OBJ#'

        m = re.search("<pre id[^>].*</pre>",context_json)
        if m is not None:
            sentence = context_json[m.start():m.end()]
            sentence = re.sub(f'<pre id="{parts}">',"",sentence)
            sentence = re.sub(r"</pre>","",sentence)
            
            # 문장부호 처리
            sentence = re.sub(r'&quot;','"',sentence)
            sentence = re.sub(r"&lt;",'<',sentence)
            sentence = re.sub(r"&gt;",'>',sentence)
            sentence = re.sub(r"&amp;",'&',sentence)
            sentence = re.sub(r"&nbsp;",'&',sentence)
            
            
            # 인덱스 정보 재추출 때문에 마커 사용
            if subj_info['start_idx'] < obj_info['start_idx']:
                s1 = subj_info['start_idx']
                s2 = obj_info['start_idx']
                e1 = subj_info['end_idx']
                e2 = obj_info['end_idx']
                t1, t2, t3 = sentence[:s1], sentence[e1:s2], sentence[e2:]
                sentence_with_entity = f"{t1}{subj_marker}{subj_info['word']}{t2}{obj_marker}{obj_info['word']}{t3}"
            else:
                s1 = obj_info['start_idx']
                s2 = subj_info['start_idx']
                e1 = obj_info['end_idx']
                e2 = subj_info['end_idx']

                t1, t2, t3 = sentence[:s1], sentence[e1:s2], sentence[e2:]

                sentence_with_entity =  f"{t1}{obj_marker}{obj_info['word']}{t2}{subj_marker}{subj_info['word']}{t3}"   


            # WORKER 제거
            sentence_with_entity = re.sub(r'WORKER[0-9]',"",sentence_with_entity)

            # 후 처리
            sentence_with_entity = re.sub(r'\s+',' ',sentence_with_entity).strip()

            # subj, obj 인덱스 재조정 및 마커 제거
            subj = re.search(subj_marker,sentence_with_entity)
            obj = re.search(obj_marker,sentence_with_entity)

            if subj.start()<obj.start():

                sentence_with_entity = re.sub(subj_marker,"",sentence_with_entity) # 마커 제거
                subj_info["start_idx"] = subj.start()
                subj_info["end_idx"] = subj.start() + len( subj_info["word"])

                obj = re.search(obj_marker,sentence_with_entity)
                sentence = re.sub(obj_marker,"",sentence_with_entity)

                obj_info["start_idx"] = obj.start()
                obj_info["end_idx"] = obj.start() + len( obj_info["word"])

            else:
                sentence_with_entity = re.sub(obj_marker,"",sentence_with_entity)
                obj_info["start_idx"] = obj.start()
                obj_info["end_idx"] = obj.start() + len( obj_info["word"])

                subj = re.search(subj_marker,sentence_with_entity)
                sentence = re.sub(subj_marker,"",sentence_with_entity)

                subj_info["start_idx"] = subj.start()
                subj_info["end_idx"] = subj.start() + len( subj_info["word"])

        return sentence, subj_info, obj_info
    
    file_ids = [file_name.split(".txt")[0] for file_name in os.listdir(ENTITY_DIR)]
    file_nums = [ids.split("-")[1] for ids in file_ids]
    relation_files = [ENTITY_DIR + "/"+ file_id + ".txt.ann.json" for file_id in file_ids]
    context_files = [SENTENCE_DIR + "/"+ file_id + ".txt.plain.html" for file_id in file_ids]
    
    
    sentence_list = []
    subj_list=[]
    obj_list = []

    for idx,(relation_file, context_file, file_num) in enumerate(zip(relation_files,context_files, file_nums)):
        #subject, object 정보 추출
        with open(relation_file, "r", encoding ="utf8") as f:
            relation_json = json.load(f)
            parts=relation_json['annotatable']['parts'][0]
            subj_info, obj_info = get_entities(relation_json)
            if subj_info is None or obj_info is None:
                print("Entity is None")
                continue
            # sentence 추출
        with open(context_file, "r", encoding ="utf8") as f:
            context_json = f.read()
            sentence, subj_info, obj_info = get_sentence(context_json, parts,subj_info,obj_info)

        subj_list.append(subj_info)
        obj_list.append(obj_info)
        sentence_list.append(sentence)



    subj_word = [i["word"] for i in subj_list]
    obj_word = [i["word"] for i in obj_list]

    subj_type = [i["type"] for i in subj_list]
    obj_type = [i["type"] for i in obj_list]

    subj_index=[]
    obj_index=[]

    for s in subj_list:
        idx = dict()
        idx["start_idx"]=s["start_idx"]
        idx["end_idx"]=s["end_idx"]
        subj_index.append(idx)

    for o in obj_list:
        idx = dict()
        idx["start_idx"]=o["start_idx"]
        idx["end_idx"]=o["end_idx"]
        obj_index.append(idx)

    relation = [""]*len(sentence_list)

    df = pd.DataFrame({'id':range(len(sentence_list)),'sentence':sentence_list,'subj_entity':subj_word,'obj_entity':obj_word,'subj_type':subj_type, 'obj_type':obj_type, 'subj_index':subj_index,'obj_index':obj_index,'relation':relation})
    
    return df


if __name__ == '__main__':
    USER_ID = input("ID : ")  # tagtog id
    USER_PW = input("PW : ")  # tagtog pw
    WORK_DIR = "final/" # 실제 json 파일이 있는 마지막 디렉터리 경로  WORKER 있던 폴더이름 넣어주세요

    # 다운로드
    o_file = file_download(USER_ID,USER_PW)
    
    # 추출
    dir_path = file_extraction(o_file)
    
    # 작업할 폴더 변경
    dir_path += "/olympics/" 
    
    context_name_list = os.listdir(dir_path + "ann.json/master/pool/final")
    print("Directory list : ", context_name_list)
    # 작업할 폴더 이름 입력
    
    WORK_DIR += input("Work Directory : ")
    
    # 데이터 정제 및 데이터 프레임 반환
    output = to_entity_csv(dir_path,WORK_DIR)
    output.to_csv('output.csv', index=False)