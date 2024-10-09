import random
from students import students
import time
import mysql.connector
from dotenv import load_dotenv  #.env 파일에서 MySQL 비��번호를 로드합니다.
import os

load_dotenv()  # .env 파일을 로드합니다.

# MySQL 연결
db = mysql.connector.connect(
    host="localhost",
    user="mgmt",
    password=os.getenv("MYSQL_PASSWORD"),
    database="memberdb"
)
cursor = db.cursor()

# 출석한 학생들만 뽑아내기
cursor.execute("SELECT student_id, name, positions, default_group, p1_count, p3_count FROM students WHERE present = 1")
attending_students = cursor.fetchall()

# 시드를 현재 시간으로 설정
random.seed(time.time())

n = len(attending_students)
k = max(1, n // 4)  # 최소 1개의 팀을 보장

# 그룹별 분류
group_Leader = [[student[0], student[1], student[4]] for student in attending_students if student[3] == "Leader"]
group_A = [[student[0], student[1], student[4], student[5]] for student in attending_students if student[3] == "A"]
group_B = [[student[0], student[1], student[4], student[5]] for student in attending_students if student[3] == "B"]
group_C = [[student[0], student[1], student[5]] for student in attending_students if student[3] == "C"]

# 각 그룹의 인원 수 출력
print(f'총 출석 학생 수: {n}')
print(f'Leader 그룹 인원: {len(group_Leader)}')
print(f'A 그룹 인원: {len(group_A)}')
print(f'B 그룹 인원: {len(group_B)}')
print(f'C 그룹 인원: {len(group_C)}')

# A그룹 인원 조정
required_A_size = 2 * k - len(group_Leader)  # A 그룹이 가져야 하는 인원 수 계산
print(required_A_size)
if len(group_A) > required_A_size:
    group_A.sort(key=lambda x: x[3])  # p3_count 기준으로 정렬
    A_to_B = group_A[required_A_size:]
    group_A = group_A[:required_A_size]
    group_B += A_to_B
elif len(group_A) < required_A_size:
    group_B.sort(key=lambda x: x[2])  # p1_count 기준으로 정렬
    B_to_A = group_B[:(required_A_size - len(group_A))]
    group_B = group_B[(required_A_size - len(group_A)):]
    group_A += B_to_A

# B그룹 인원 조정
if len(group_B) > k:
    group_B.sort(key=lambda x: x[3])
    B_to_C = group_B[k:]
    group_B = group_B[:k]
    group_C += B_to_C
elif len(group_B) < k:
    group_C.sort(key=lambda x: x[2])
    C_to_B = group_C[:(k - len(group_B))]
    group_C = group_C[(k - len(group_B)):]
    group_B += C_to_B

# 각 그룹 조정 후 인원 수 출력
print(f'조정 후 Leader 그룹 인원: {len(group_Leader)}')
print(f'조정 후 A 그룹 인원: {len(group_A)}')
print(f'조정 후 B 그룹 인원: {len(group_B)}')
print(f'조정 후 C 그룹 인원: {len(group_C)}')

# 조를 나누기 위한 pot 배정
group_Leader.sort(key=lambda x: x[2])

# p1_count가 낮은 k명을 1포트에 배정
pot_1 = [group_Leader[i] for i in range(min(k, len(group_Leader)))]
# 코어 인원이 k보다 많을 경우 2포트로 일부 배정
pot_2 = group_Leader[k:] if len(group_Leader) > k else []

# A그룹 인원 처리
pot_1 += [student for student in group_A[:k - len(pot_1)]]
pot_2 += group_A[k - len(pot_1):]

# C그룹에서 p3_count 낮은 k명을 3포트에 배정
group_C.sort(key=lambda x: x[2])
pot_3 = [group_C[i] for i in range(min(k, len(group_C)))]
remaining_C = group_C[k:]

# 각 pot 인원 수 출력
print(f'Pot 1 인원 수: {len(pot_1)}')
print(f'Pot 2 인원 수: {len(pot_2)}')
print(f'Pot 3 인원 수: {len(pot_3)}')
print(f'Remaining C 인원 수: {len(remaining_C)}')

random.shuffle(pot_1)
random.shuffle(pot_2)
random.shuffle(group_B)
random.shuffle(pot_3)

# R페어와 S페어에서 한 팀씩 만들 때 인덱스 에러 처리
pair_R = []
pair_S = []

# pair_R 생성
for i in range(min(k, len(pot_1), len(pot_2))):
    pair_R.append((pot_1[i], pot_2[i]))

# pair_S 생성 (이 부분도 같은 방식으로 처리)
for i in range(min(k, len(group_B), len(pot_3))):
    pair_S.append((group_B[i], pot_3[i]))

# 나머지 그룹 묶기
random_scrum = [[list(pair_R[i]) + list(pair_S[i])] for i in range(len(pair_R))]

print(k)

# 팀별 출력
for i in range(len(pair_R)):
    print(f'Team {i+1}')
    for student in random_scrum[i]:
        print(f'{student[0][1]}: {student[1][1]}, {student[2][1]}, {student[3][1]}')
    print()

# 남은 C그룹 학생 랜덤 팀 배정
if remaining_C:
    random_teams = random.sample(range(1, k + 1), len(remaining_C))  # 남은 학생 수만큼 팀 선택
    for i in range(len(remaining_C)):
        print(f'{remaining_C[i][1]} -> Team {random_teams[i]}')


    # print(f'{remaining_C[i][1]}({remaining_C[i][0]} -> Team {random_team})')


# 완전히 구현하지 못한 것들:
'''
- 팀 스크럼을 같이 하는 사람들끼리는 가급적 같은 조가 되지 않는다.
- 한번 같은 페어가 됐던 사람들끼리는 k회동안 같은 조가 되지 않는다.
- DB 연결
- Web으로 결과 표시
'''