import pandas as pd
import os
import re
import html
import json

# ./olympics/ann.json/master/pool/pilot/
# a_ycW7OyVT2Mp06ECMv5zgi0ULe8-text.txt.ann.json
# ./olympics/plain.html/pool/pilot/
# a_ycW7OyVT2Mp06ECMv5zgi0ULe8-text.txt.plain.html

ENTITY_DIR = "./olympics/ann.json/master/pool/pilot/"
SENTENCE_DIR = "./olympics/plain.html/pool/pilot/"


def get_context_from_html(html_file):
    html_file = re.sub(r"\n","", html_file)
    html_file = html.unescape(html_file) # 21-11-17 추가, &quot; 등 제거
    return re.findall("(<pre.+>)(.+)(</pre>)",html_file)[0][1]


def get_sentence(file_id):

    with open(SENTENCE_DIR + file_id + "-text.txt.plain.html", "r") as f:
        sentence_file = f.read()

    sentence = get_context_from_html(sentence_file)

    return sentence


"""entity = {
    "classId":"e_3",
    "part":"s1v1",
    "offsets":[{"start":5,"text":"올림픽"}],
    "coordinates":[],
    "confidence":{"state":"pre-added","who":["user:bongseok"],"prob":1},
    "fields":{},
    "normalizations":{}
}"""

def get_entities(file_id, annotation_legend):

    with open(ENTITY_DIR + file_id + "-text.txt.ann.json", "r") as f:
        entity_json = json.load(f)
    
    temp1, temp2 = entity_json['entities']

    if annotation_legend[temp1['classId']][:4] == "SUBJ":
        subj_temp = temp1
        obj_temp = temp2
    else:
        subj_temp = temp2
        obj_temp = temp1

    subj = {
        'type': annotation_legend[subj_temp['classId']],
        'start': subj_temp['offsets'][0]['start'],
        'text': subj_temp['offsets'][0]['text']
    }
    subj['end'] = subj['start'] + len(subj['text'])

    obj = {
        'type': annotation_legend[obj_temp['classId']],
        'start': obj_temp['offsets'][0]['start'],
        'text': obj_temp['offsets'][0]['text']
    }
    obj['end'] = obj['start'] + len(obj['text'])

    return subj, obj


def mark_entities(subj, obj, sentence):

    if subj['start'] < obj['start']:
        s1 = subj['start']
        s2 = obj['start']
        e1 = subj['end']
        e2 = obj['end']

        t1, t2, t3 = sentence[:s1], sentence[e1:s2], sentence[e2:]

        sentence_with_entity = f"{t1}<SUBJ:{subj['text']}>{t2}<OBJ:{obj['text']}>{t3}"
    else:
        s1 = obj['start']
        s2 = subj['start']
        e1 = obj['end']
        e2 = subj['end']

        t1, t2, t3 = sentence[:s1], sentence[e1:s2], sentence[e2:]

        sentence_with_entity = f"{t1}<OBJ:{obj['text']}>{t2}<SUBJ:{subj['text']}>{t3}"


    return sentence_with_entity


def get_csv(folder_path):
    id_list = []
    sentence_list = []
    subj_type_list = []
    obj_type_list = []

    annotation_legend = folder_path + "/annotations-legend.json"
    with open(annotation_legend,"r") as f:
        annotation_legend = json.load(f)
    
    file_name_list = os.listdir(folder_path + '/plain.html/pool/pilot')

    file_id_list = [file_name.split('-')[0] for file_name in file_name_list]

    for i, file_id in enumerate(file_id_list):
        id_list.append(i+1)

        sentence = get_sentence(file_id)
        subj, obj = get_entities(file_id, annotation_legend)

        subj_type_list.append(subj['type'])
        obj_type_list.append(obj['type'])

        sentence_with_entity = mark_entities(subj, obj, sentence)

        sentence_list.append(sentence_with_entity)

    
    df = pd.DataFrame({
        "id": id_list,
        'sentence': sentence_list,
        'subj_type': subj_type_list,
        'obj_type': obj_type_list,
    })

    df.to_csv('test.csv', index=False)
    return 0


if __name__ == '__main__':
    get_csv('./olympics')