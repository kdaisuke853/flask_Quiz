from flask import Flask, render_template, request
import mysql.connector as mydb
import re

# クイズのデータベースに接続(phpmyadmin)
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

# 問題文・選択肢・答え等のカテゴリに分類

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
bad_ans = []

app = Flask(__name__)


# トップ画面
@app.route('/')
def index():
    bad_ans.clear()  # 間違った問題リストをクリアして空にする。
    catg = 0
    return render_template('index.html')


# 問題文表示
@app.route('/mondai', methods=['POST', 'GET'])
def mondai():
    try:
        if request.method == 'POST':
            q_id = int(request.form['q_id'])
        elif request.method == 'GET':
            q_id = request.args.get('id', '', type=int)

    except Exception as e:
        return str(e)
    """
    # 文字数短縮のため置き換え(置き換え無くても動く)
    q_question = question_question
    q_questionA = question_A
    q_questionB = question_B
    q_questionC = question_C
    q_questionD = question_D
    q_questionE = question_E
    q_questionF = question_F
    q_answer = question_answer
    """
    catg = '0'
    # 問題文が複数選択の場合(問題文の中に[2つ選択]がある場合)
    if re.search(r'つ選択', q_question[q_id]):
        # チェックボックス形式のHTMLを呼び出す
        return render_template('mondai_sentaku.html', q_id=q_id, t_id=q_id, q_question=question_question[q_id],
                               q_question1=question_A[q_id], q_question2=question_B[q_id], q_question3=question_C[q_id],
                               q_question4=question_D[q_id], q_question5=question_E[q_id], q_question6=question_F[q_id],
                               q_answer=question_answer[q_id], catg=catg)
    else:
        # ラジオボタン形式のHTMLを呼び出す
        return render_template('mondai.html', q_id=q_id, t_id=q_id, q_question=q_question[q_id],
                               q_question1=q_questionA[q_id],
                               q_question2=q_questionB[q_id],
                               q_question3=q_questionC[q_id], q_question4=q_questionD[q_id],
                               q_question5=q_questionE[q_id], q_question6=q_questionF[q_id], q_answer=q_answer[q_id],
                               catg=catg)


"""
    return render_template('mondai.html', q_id=q_id, t_id=q_id, q_question=q_question, q_question1=q_question_A,
                           q_question2=q_question_B,
                           q_question3=q_questionC, q_question4=q_questionD, q_question5=q_questionE,
                           q_question6=q_questionF, q_answer=q_answer, catg=catg)
"""


# 答え合わせ(ラジオボタン形式)
@app.route('/answer', methods=['POST'])
def answer():
    judge = 0
    try:
        if request.method == 'POST':
            post_answer = request.form.get('q')
            t_id = int(request.form.get('t_id'))
            # post_myans = request.form.get('q')
            post_id = int(request.form.get('q_id'))
    except Exception as e:
        return str(e)
    # postされた値と答えが一致していたら正解
    if question_answer[post_id] == post_answer:
        judge = "正解"
    # 違ったら不正解、間違った問題リストに入れる
    elif question_answer[post_id] != post_answer:
        judge = "不正解"
        T_id = post_id
        bad_ans.append(T_id)

    return render_template('answer.html', judge=judge, post_id=post_id, t_id=t_id, answer=question_answer[post_id],
                           post_answer=post_answer, bad_ans=bad_ans, q_question=question_question[post_id],
                           q_question1=question_A[post_id], q_question2=question_B[post_id],
                           q_question3=question_C[post_id], q_question4=question_D[post_id],
                           q_question5=question_E[post_id], q_question6=question_F[post_id])


# 答え合わせ(チェックボタン形式[複数選択形式])
@app.route('/answer2', methods=['POST'])
def answer2():
    judge = 0
    try:
        if request.method == 'POST':
            # p_ans.append(request.form.get('check[]'))
            post_answer = request.form.getlist('check[]')
            p_ans = ''.join(post_answer)
            # t_id = int(request.form.get('t_id'))
            post_id = int(request.form.get('q_id'))
            t_id = request.form.get('t_id')


    except Exception as e:
        return str(e)

    post_answer = p_ans

    if question_answer[post_id] == post_answer:
        judge = "正解"
    elif question_answer[post_id] != post_answer:
        judge = "不正解"
        T_id = post_id
        bad_ans.append(T_id)

    return render_template('answer.html', judge=judge, post_id=post_id, answer=question_answer[post_id],
                           post_answer=post_answer, p_ans=p_ans, bad_ans=bad_ans,
                           q_question=question_question[post_id], t_id=t_id,
                           q_question1=question_A[post_id], q_question2=question_B[post_id],
                           q_question3=question_C[post_id], q_question4=question_D[post_id],
                           q_question5=question_E[post_id], q_question6=question_F[post_id]
                           )


# 間違えた問題に再挑戦する場合
@app.route('/mondai_bad', methods=['POST', 'GET'])
def mondai_bad():
    try:
        if request.method == 'POST':
            t_id = request.form.get('t_id')
    except Exception as e:
        return str(e)

    # q_2 = []
    q_id = bad_ans[0]
    bad_ans.pop(0)
    """
    q_question = question_question
    q_questionA = question_A
    q_questionB = question_B
    q_questionC = question_C
    q_questionD = question_D
    q_questionE = question_E
    q_questionF = question_F
    q_answer = question_answer
    """

    if re.search(r'つ選択', question_question[q_id]):
        return render_template('mondai_sentaku_bad.html', q_id=q_id, t_id=t_id, q_question=question_question[q_id],
                               q_question1=question_A[q_id], q_question2=question_B[q_id], q_question3=question_C[q_id],
                               q_question4=question_D[q_id], q_question5=question_E[q_id], q_question6=question_F[q_id],
                               q_answer=question_answer[q_id])
    else:
        return render_template('mondai_bad.html', q_id=q_id, t_id=t_id, q_question=question_question[q_id],
                               q_question1=question_A[q_id], q_question2=question_B[q_id],
                               q_question3=question_C[q_id], q_question4=question_D[q_id],
                               q_question5=question_E[q_id], q_question6=question_F[q_id],
                               q_answer=question_answer[q_id])
    """
    return render_template('mondai_bad.html', q_id=q_id, t_id=t_id, q_question=q_question, q_question1=q_question_A,
                           q_question2=q_question_B,
                           q_question3=q_questionC, q_question4=q_questionD, q_question5=q_questionE,
                           q_question6=q_questionF, q_answer=q_answer)
    """


# 間違えた問題の回答(複数選択形式)
@app.route('/answer2_bad', methods=['POST'])
def answer2_bad():
    judge = 0
    try:
        if request.method == 'POST':
            # p_ans.append(request.form.get('check[]'))
            post_answer = request.form.getlist('check[]')
            p_ans = ''.join(post_answer)
            # t_id = request.form.get('t_id')
            # print(t_id)
            t_id = int(request.form.get('t_id'))
            post_id = int(request.form.get('q_id'))
            # post_id = request.form.get('q_id')

    except Exception as e:
        return str(e)

    post_answer = p_ans

    if question_answer[post_id] == post_answer:
        judge = "正解"
    elif question_answer[post_id] != post_answer:
        judge = "不正解"
        T_id = post_id
        bad_ans.append(T_id)

    return render_template('answer_bad.html', judge=judge, post_id=post_id, t_id=t_id, answer=question_answer[post_id],
                           post_answer=post_answer, p_ans=p_ans, bad_ans=bad_ans,
                           q_question=question_question[post_id],
                           q_question1=question_A[post_id], q_question2=question_B[post_id],
                           q_question3=question_C[post_id], q_question4=question_D[post_id],
                           q_question5=question_E[post_id], q_question6=question_F[post_id]
                           )


# 間違えた問題の回答(ラジオボタン形式)
@app.route('/answer_bad', methods=['POST'])
def answer_bad():
    judge = 0
    try:
        if request.method == 'POST':
            post_answer = request.form.get('q')
            t_id = int(request.form.get('t_id'))
            # post_myans = request.form.get('q')
            post_id = int(request.form.get('q_id'))
    except Exception as e:
        return str(e)

    if question_answer[post_id] == post_answer:
        judge = "正解"
    elif question_answer[post_id] != post_answer:
        judge = "不正解"
        T_id = post_id
        bad_ans.append(T_id)

    return render_template('answer_bad.html', judge=judge, post_id=post_id, t_id=t_id, answer=question_answer[post_id],
                           post_answer=post_answer, bad_ans=bad_ans, q_question=question_question[post_id],
                           q_question1=question_A[post_id], q_question2=question_B[post_id],
                           q_question3=question_C[post_id], q_question4=question_D[post_id],
                           q_question5=question_E[post_id], q_question6=question_F[post_id])


# カテゴリ別問題(EC2)
@app.route('/cat', methods=['POST'])
def cat():
    EC2_count = len(question_EC2)
    return render_template('categoly.html', EC2_count=EC2_count)


# カテゴリ別問題文(EC2)
@app.route('/cat/EC2', methods=['POST'])
def ec2_test():
    q_id = question_EC2[0] - 1
    question_EC2.pop(0)

    """
    q_question = question_question
    q_questionA = question_A
    q_questionB = question_B
    q_questionC = question_C
    q_questionD = question_D
    q_questionE = question_E
    q_questionF = question_F
    q_answer = question_answer
    """
    catg = '1'

    if re.search(r'つ選択', question_question[q_id]):
        return render_template('mondai_sentaku.html', q_id=q_id, q_question=question_question[q_id],
                               q_question1=question_A[q_id], q_question2=question_B[q_id],
                               q_question3=question_C[q_id], q_question4=question_D[q_id],
                               q_question5=question_E[q_id], q_question6=question_F[q_id],
                               q_answer=question_answer[q_id], catg=catg)
    else:
        return render_template('mondai.html', q_id=q_id, q_question=question_question[q_id],
                               q_question1=question_A[q_id],q_question2=question_B[q_id],
                               q_question3=question_C[q_id], q_question4=question_D[q_id],
                               q_question5=question_E[q_id], q_question6=question_F[q_id], q_answer=question_answer[q_id],
                               catg=catg)

    return render_template('mondai.html', q_id=q_id, q_question=q_question, q_question1=q_question_A,
                           q_question2=q_question_B,
                           q_question3=q_questionC, q_question4=q_questionD, q_question5=q_questionE,
                           q_question6=q_questionF, q_answer=q_answer, catg=catg)

#カテゴリ問題回答
@app.route('/cat/answer', methods=['POST'])
def answer_cat():
    judge = 0
    try:
        if request.method == 'POST':
            post_answer = request.form.get('q')
            # t_id = int(request.form.get('t_id'))
            # post_myans = request.form.get('q')
            post_id = int(request.form.get('q_id'))
    except Exception as e:
        return str(e)

    if question_answer[post_id] == post_answer:
        judge = "正解"
    elif question_answer[post_id] != post_answer:
        judge = "不正解"
        T_id = post_id
        bad_ans.append(T_id)

    return render_template('answer_cat.html', judge=judge, post_id=post_id, answer=question_answer[post_id],
                           post_answer=post_answer, bad_ans=bad_ans, q_question=question_question[post_id],
                           q_question1=question_A[post_id], q_question2=question_B[post_id],
                           q_question3=question_C[post_id], q_question4=question_D[post_id],
                           q_question5=question_E[post_id], q_question6=question_F[post_id])


if __name__ == '__main__':
    app.run(debug=True)
