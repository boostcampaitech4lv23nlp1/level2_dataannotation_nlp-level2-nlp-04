import pickle as pickle


def label_to_num(label):
    """
    문자열 라벨을 숫자로 변환 합니다.
    """
    num_label = []
    dict_label_to_num = {"관계_없음":0,
        "인물:참가":1,
        "인물:소속":2,
        "인물:결과":3,
        "단체:결과":4,
        "단체:참가":5,
        "행사:장소":6,
        "행사:일시":7,
        "행사:하위_행사":8}
    for v in label:
        num_label.append(dict_label_to_num[v])

    return num_label


def num_to_label(label):
    """
    숫자로 되어 있던 class를 원본 문자열 라벨로 변환 합니다.
    """
    origin_label = []
    dict_num_to_label = { 0:"관계_없음",
        1:"인물:참가",
        2:"인물:소속",
        3:"인물:결과",
        4:"단체:결과",
        5:"단체:참가",
        6:"행사:장소",
        7:"행사:일시",
        8:"행사:하위_행사"}
    for v in label:
        origin_label.append(dict_num_to_label[v])

    return origin_label
