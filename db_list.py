import mysql.connector as mydb
import re

conn = mydb.connect(
    host='localhost',
    user='root',
    port='3306',
    password='',
    database='mydb'
)

cur = conn.cursor()
cur.execute("SELECT * FROM aws_exam")
# 全てのデータを取得
rows = cur.fetchall()

question_id = []
question_question = []
question_A = []
question_B = []
question_C = []
question_D = []
question_E = []
question_F = []
question_answer = []
question_EC2 = []

x = 0
while x < len(rows):
    question_id.append(rows[x][0])
    # 問題文を代入
    question_question.append(rows[x][1])
    if re.search(r'EC2', rows[x][1]):
        question_EC2.append(rows[x][0])
        print(rows[x][1])
    # 選択肢1を代入
    question_A.append(rows[x][2])
    # 選択肢2を代入
    question_B.append(rows[x][3])
    # 選択肢3を代入
    question_C.append(rows[x][4])
    # 選択肢4を代入
    question_D.append(rows[x][5])
    # 答えを代入
    question_E.append(rows[x][6])

    question_F.append(rows[x][7])
    # 答えを代入
    question_answer.append(rows[x][8])

    x += 1

cur.close()
conn.close()
print(question_EC2)