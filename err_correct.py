import re

sentence= '같은 날 아베 신조 당시 일본 총리는 "선수들의 안전 확보가 가장 중요하다"며 연기하는 방안을 지지하겠다고 밝혔고, 전 IOC 위원딕 파운드부회장인 딕 파운드(Dick Pound)도 올림픽이 연기될 것으로 예상한다고 말했다.'
sub_entity = "딕 파운드"
obj_entity = "IOC"

# {'start_idx': 73, 'end_idx': 78}
sub = re.search(sub_entity,sentence)
obj = re.search(obj_entity,sentence)
print('\n')
print("{'start_idx':%d , 'end_idx': %d}\t\t\t\tsubject" %(sub.start(),sub.end()))
print('\n')
print("{'start_idx':%d , 'end_idx': %d}\t\t\t\tobject" %(obj.start(),obj.end()))

