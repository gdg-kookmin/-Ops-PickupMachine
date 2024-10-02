import random
from students import students
import time

# 시드를 현재 시간으로 설정
random.seed(time.time())

n = len(students)
k = n//4

# 그룹별 분류
group_Leader = [[student.student_id, student.name, student.p1_count] for student in students if student.group == "Leader"]
group_A = [[student.student_id, student.name, student.p1_count] for student in students if student.group == "A"]
group_B = [[student.student_id, student.name] for student in students if student.group == "B"]
group_C = [[student.student_id, student.name, student.p3_count] for student in students if student.group == "C"]
random.shuffle(group_Leader) # DB 만들면 이 부분 삭제
random.shuffle(group_C) # DB 만들면 이 부분 삭제

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

random.shuffle(pot_1)
random.shuffle(pot_2)
random.shuffle(group_B)
random.shuffle(pot_3)

# 1포트-2포트, B그룹-3포트 학생 묶기
pair_R = [(pot_1[i], pot_2[i]) for i in range(k)]
pair_S = [(group_B[i], pot_3[i]) for i in range(k)]
'''
# 페어로 묶였다는 기록
for i in range(k):
    pot_1[i].paired_students.add(pot_2[i].student_id)
    pot_2[i].paired_students.add(pot_1[i].student_id)
    group_B[i].paired_students.add(pot_4[i].student_id)
    pot_4[i].paired_students.add(group_B[i].student_id)
'''

# 랜덤 스크럼 조 편성
random_scrum = []

# R페어와 S페어에서 한 팀씩
random_scrum = [[list(pair_R[i])+list(pair_S[i])] for i in range(k)]

# 팀별 출력
for i in range(k):
    print(f'Team {i+1}')
    for student in random_scrum[i]:
        print(
            f'{student[0][1]}: {student[1][1]}, {student[2][1]}, {student[3][1]}')
            # print(f'{student[0][1]}({student[0][0]}): {student[1][1]}({student[1][0]}), {student[2][1]}({student[2][0]}), {student[3][1]}({student[3][0]})')
    print()

random_teams = random.sample(range(1, k), 2)

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