######### mersombre-2021-1-db-app #########

import psycopg2
from flask import Flask, render_template, request

app = Flask(__name__)

connect = psycopg2.connect("dbname=flask user=postgres password=0513")
cur = connect.cursor()


@app.route('/')
def main():
    return render_template("login.html")

@app.route('/signup', methods=['POST'])
def signup():
    return render_template("sign_up_page.html")

#sign up page. html
@app.route('/idcheck', methods=['POST'])
def idcheck():
    id = request.form["id"]
    cur.execute("select id from member where id = '{}';" .format(id))
    findid = cur.fetchall()
    print(findid)
    try:
        if id == findid[0][0]:
            return "아이디 중복 / 다시 확인"
    except IndexError:
        return render_template("sign_up_page.html")


@app.route('/newmember', methods=['POST'])
def newmember():
    id = request.form["id"]
    name = request.form["name"]
    cur.execute("insert into member values('{}', '{}');" .format(id, name))
    connect.commit()
    return "가입 완료 / 이전 화면으로 돌아가 로그인하세요"

@app.route('/backlogin', methods=['POST'])
def backlogin():
    return render_template("login.html")



#관리자 메뉴
@app.route('/forworker', methods=['POST'])
def forworker():
    return render_template("forworker.html")

@app.route('/mbmanage', methods=['POST'])
def mbmanage():
    id = request.form['id']
    cur.execute("select id from member where id = '{}';" .format(id))
    delid = cur.fetchall()

    try:
        if id == delid[0][0]:
            cur.execute("delete from member where id = '{}';" .format(id))
            connect.commit()
            return "해당 휴면회원이 삭제되었습니다."
    except IndexError:
        return "입력된 회원 id를 다시 확인해주세요."

@app.route('/bookmanage', methods=['POST'])
def bookmanage():
    bookid = request.form['bookid']
    cur.execute("select book_id, books.cf_num, cf_name from books, classification where books.cf_num = classification.cf_num and book_id = {};" .format(bookid))
    bookmg = cur.fetchall()

    try:
        if bookid == str(bookmg[0][0]):
            return render_template("bookmanage.html", bookmanage = bookmg)
    except IndexError:
        return "입력된 도서 id를 다시 확인해주세요."

@app.route('/borrower', methods=['POST'])
def borrowermanage():

    cur.execute("select id, book_id, borrow, return from member natural join borrow order by borrow;")
    borrowermg = cur.fetchall()

    return render_template("borrowerinfo.html", borrower = borrowermg)

@app.route('/workers', methods=['POST'])
def workermanage():

    cur.execute("select dept, (select count(*) from worker where worker.dept = department.dept) from department;")
    workermg = cur.fetchall()

    return render_template("workerinfo.html", worker = workermg)



#로그인
@app.route('/login', methods=['POST'])
def login():
    id = request.form['id']
    name = request.form['name']
    cur.execute("select id, name from member where id = '{}' and name = '{}'" .format(id, name))
    result = cur.fetchall()

    try:
        if id == result[0][0] and name == result[0][1]:
            return render_template("home.html")
    except:
        return "ID나 회원명 다시 확인하세요"


# 제목 검색
@app.route('/findbook', methods=['POST'])
def findbook():
    findtitle = request.form['title']
    cur.execute("select * from books where title like '%{}%';" .format(findtitle))
    titleresult = cur.fetchall()

    try:
        if findtitle == titleresult[0][2]:
            return render_template("findbook.html", findtitle=titleresult)
    except IndexError:
        return "찾는 책이 없습니다. 제목을 다시 확인해주세요"


# 재고 현황
@app.route('/findbooknum', methods=['POST'])
def findbooknum():
    title = request.form['title2']
    cur.execute("select count(title) from books where title = '{}';" .format(title))
    result = cur.fetchall()

    if result[0][0] != 0:
        return str(result[0][0])
    else: return "현재 도서관에 구비되어 있지 않습니다."

# 대출연장
@app.route('/borrowmore', methods=['POST'])
def borrowmore():
    id = request.form['id']
    bookid = request.form['bookid']
    cur.execute("select id, book_id from borrow where id = '{}' and book_id = '{}';".format(id, bookid))
    result = cur.fetchall()

    try:
        if id == result[0][0] and bookid == str(result[0][1]):
            cur.execute("update borrow set return = return + interval '14 day' where id = '{}' and book_id = '{}';".format(id, bookid))
            connect.commit()
            cur.execute("select * from borrow where id = '{}' and book_id = '{}';".format(id, bookid))
            tableresult = cur.fetchall()
        return render_template("borrowmore.html", more = tableresult)

    except IndexError: return "찾는 책이 없습니다. 회원 id나 도서 id를 다시 확인해주세요"

if __name__ == '__main__':
    app.run()
