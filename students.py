'''
전체 인원수가 n이고, int k = n/4일 때,
- "Leader"그룹과 "A"그룹의 인원 합은 반드시 2k여야 한다.
- "B"그룹의 인원은 반드시 k명이어야 한다.
'''

import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# 학생 데이터 저장할 구조체 정의
class Student:
    def __init__(self, student_id, name, positions, group, p1_count=0, p3_count=0):
        self.student_id = student_id
        self.name = name
        self.group = group
        self.positions = positions if isinstance(positions, list) else [positions]  # 리스트로 처리
        self.p1_count = p1_count
        self.p3_count = p3_count
        self.paired_students = set()

students = [
    Student("20225209", "권영후", "Core", "Leader", 0, 0),
    Student("20223152", "최승훈", "Core", "Leader", 0, 0),
    Student("20000003", "송유나", "Core", "Leader", 0, 0),
    Student("20222038", "김세현", "Core", "Leader", 0, 0),
    Student("20000005", "박성훈", "Core", "Leader", 0, 0),
    Student("20215215", "한승민", "Core", "Leader", 0, 0),
    Student("20243025", "김동훈", "Core", "Leader", 0, 0),
    Student("20212670", "고다연", "Core", "Leader", 0, 0),
    Student("20000009", "윤신지", "Core", "Leader", 0, 0),
    Student("20000010", "성재승", "Core", "Leader", 0, 0),
    Student("20000011", "김진재", "Core", "Leader", 0, 0),
    Student("20000012", "송보경", "Core", "Leader", 0, 0),
    Student("20000013", "김종민", "Core", "Leader", 0, 0),
    Student("20000014", "이나경", "Dev_J", "A", 0, 0),
    Student("20225225", "나성민", "Dev_G", "A", 0, 0),
    Student("20213196", "김민성", "Dev_J", "A", 0, 0),
    Student("20233091", "임태근", "Dev_G", "A", 0, 0),
    Student("20233000", "조혜림", ["Dev_J", "Design"], "A", 0, 0),
    Student("20215184", "박여명", "Dev_G", "A", 0, 0),
    Student("20243047", "김형민", "Dev_J", "A", 0, 0),
    Student("20233049", "박유나", "Dev_G", "B", 0, 0),
    Student("20233043", "레일라", "Dev_J", "B", 0, 0),
    Student("20203350", "신관우", "Dev_G", "B", 0, 0),
    Student("20242882", "정이안", "Dev_J", "B", 0, 0),
    Student("20213069", "임수민", "Dev_G", "B", 0, 0),
    Student("20232871", "정다연", "Dev_J", "B", 0, 0),
    Student("20215185", "신경남", "Dev_G", "B", 0, 0),
    Student("20242824", "김서현", "Dev_J", "B", 0, 0),
    Student("20213069", "이준우", "Dev_G", "B", 0, 0),
    Student("20223428", "김예찬", "Dev_J", "C", 0, 0),
    Student("20000031", "이주엽", "Dev_G", "C", 0, 0),
    Student("20243455", "이수현", "Dev_J", "C", 0, 0),
    Student("20000033", "김주은", "Dev_G", "C", 0, 0),
    Student("20233152", "이윤서", "Dev_J", "C", 0, 0),
    Student("20000035", "이동언", "Dev_G", "C", 0, 0),
    Student("20200294", "김희주", "Dev_J", "C", 0, 0),
    Student("20000037", "강태현", "Dev_G", "C", 0, 0),
    Student("20000038", "백승원", "Design", "C", 0, 0),
    Student("20000039", "이연우", "Design", "C", 0, 0),
    Student("20000040", "고혜진", "Design", "C", 0, 0),
    Student("20000041", "장연우", "Design", "C", 0, 0),
    Student("20000042", "김민제", "Design", "C", 0, 0),
    Student("20000043", "김승주", "Design", "C", 0, 0)
]

# 중복된 학생을 제거
seen_students = set()
cleaned_students = []
for student in students:
    student_key = (student.student_id, student.name)
    if student_key not in seen_students:
        cleaned_students.append(student)
        seen_students.add(student_key)

# MySQL 데이터베이스에 연결
conn = mysql.connector.connect(
    host="localhost",
    user="mgmt",  # 새로 생성한 사용자
    password=os.getenv("MYSQL_PASSWORD"),
    database="memberdb"
)

cursor = conn.cursor()

# 학생 데이터를 삽입할 쿼리
insert_query = """
    INSERT INTO students (student_id, name, positions, default_group, p1_count, p3_count)
    VALUES (%s, %s, %s, %s, %s, %s)
"""

# 중복 삽입을 피하기 위해 기존 학생 체크
for student in students:
    for position in student.positions:
        # 해당 학생이 이미 존재하는지 체크
        cursor.execute("SELECT COUNT(*) FROM students WHERE student_id = %s AND name = %s",
                       (student.student_id, student.name))
        count = cursor.fetchone()[0]

        if count == 0:  # 중복이 아닐 경우만 삽입
            cursor.execute(insert_query, (
            student.student_id, student.name, position, student.group, student.p1_count, student.p3_count))

# 변경 사항을 커밋
conn.commit()

# 연결 종료
cursor.close()
conn.close()