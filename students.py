'''
전체 인원수가 n이고, int k = n/4일 때,
- "Leader"그룹과 "A"그룹의 인원 합은 반드시 2k여야 한다.
- "B"그룹의 인원은 반드시 k명이어야 한다.
'''
# 학생 데이터 저장할 구조체 정의
class Student:
    def __init__(self, student_id, name, position, group, p1_count=0, p3_count=0):
        # 향후 p1_count와 p3_count는 DB에 저장되게 해야 함
        self.student_id = student_id
        self.name = name
        self.position = position
        self.group = group
        self.p1_count = p1_count
        self.p3_count = p3_count
        self.paired_students = set() # 이미 pair로 엮여본 사람을 저장. 추후 구현 예정

students = [
    Student("20010001", "권영후", "Core", "Leader", 0, 0),
    Student("20010002", "윤신지", "Core", "Leader", 0, 0),
    Student("20010003", "최승훈", "Core", "Leader", 0, 0),
    Student("20010004", "김세현", "Core", "Leader", 0, 0),
    Student("20010005", "박성훈", "Core", "Leader", 0, 0),
    Student("20010006", "한승민", "Core", "Leader", 0, 0),
    Student("20010007", "김동훈", "Core", "Leader", 0, 0),
    Student("20010008", "고다연", "Core", "Leader", 0, 0),
    Student("20010009", "성재승", "Core", "Leader", 0, 0),
    Student("20010010", "송보경", "Core", "Leader", 0, 0),
    Student("20010011", "김종민", "Core", "Leader", 0, 0),
    Student("20010012", "나성민", "Dev_G", "A", 0, 0),
    Student("20010013", "이나경", "Dev_J", "A", 0, 0),
    Student("20010014", "박여명", "Dev_G", "A", 0, 0),
    Student("20010015", "김민성", "Dev_J", "A", 0, 0),
    Student("20010016", "임태근", "Dev_G", "A", 0, 0),
    Student("20010017", "레일라", "Dev_J", "B", 0, 0),
    Student("20010018", "박유나", "Dev_G", "B", 0, 0),
    Student("20010019", "정이안", "Dev_J", "B", 0, 0),
    Student("20010020", "신관우", "Dev_G", "B", 0, 0),
    Student("20010021", "정다연", "Dev_J", "B", 0, 0),
    Student("20010022", "임수민", "Dev_G", "B", 0, 0),
    Student("20010023", "김서현", "Dev_J", "B", 0, 0),
    Student("20010024", "강태현", "Dev_G", "B", 0, 0),
    Student("20010025", "김예찬", "Dev_J", "C", 0, 0),
    Student("20010026", "김주은", "Dev_G", "C", 0, 0),
    Student("20010027", "이수현", "Dev_J", "C", 0, 0),
    Student("20010028", "이동언", "Dev_G", "C", 0, 0),
    Student("20010029", "이윤서", "Dev_J", "C", 0, 0),
    Student("20010030", "이주엽", "Dev_G", "C", 0, 0),
    Student("20010031", "김희주", "Dev_J", "C", 0, 0),
    Student("20010032", "이준우", "Dev_G", "C", 0, 0),
    Student("20010033", "김형민", "Dev_J", "C", 0, 0),
    Student("20010034", "신경남", "Dev_G", "C", 0, 0)
]