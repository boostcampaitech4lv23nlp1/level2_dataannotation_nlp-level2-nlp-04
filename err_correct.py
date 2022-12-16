import re

sentence= '6일간의 봉송 끝에 성화는 4월 27일 아테네 파나티나이코 스타디움에서 열린 기념식에서 브라질 조직위원들에게 전달됐다.'
sub_entity = "봉송"
obj_entity = "아테네 파나티나이코 스타디움"

# # {'start_idx': 73, 'end_idx': 78}
sub = re.search(sub_entity,sentence)
obj = re.search(obj_entity,sentence)
print('\n')
print("{'start_idx': %d , 'end_idx': %d}\t\t\t\tsubject" %(sub.start(),sub.end()))
print('\n')
print("{'start_idx': %d , 'end_idx': %d}\t\t\t\tobject" %(obj.start(),obj.end()))
