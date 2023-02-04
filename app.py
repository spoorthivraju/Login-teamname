import psycopg2
from flask import Flask, render_template, request, redirect, url_for, render_template, session, send_from_directory, send_file, flash, abort, make_response
import decimal
import itertools 
from otp import send_email, generateOtp
from db import insert
from security_questions import questions, get_random_ques

app = Flask(__name__)
#Can use this to connect it to our database
try:
    db = psycopg2.connect(database="team_a", user = "postgres", password="your_postgres_pswd")
except:
    print("not connected")
    exit()
cur = db.cursor()

@app.route('/home', methods=['POST', 'GET'])
def logout():
    return render_template("sample.html")

@app.route('/', methods=['GET'])
def register():
    if request.method == "GET":
        q = questions()
        return render_template("register.html", q=q)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")

@app.route('/otp', methods=['GET', 'POST'])
def otp():
    if request.method == "GET":
        email = session['email']
        send_email(email)
        return render_template("sample.html", msg="sent email to" + email)

@app.route('/security-ques', methods=['GET', 'POST'])
def security_ques():
    if request.method == "GET":
        d = get_random_ques()
        session["d"] = d
        print(d, list(d.items()))
        return render_template("security_ques.html", q = list(d.items()))
    elif request.method == "POST":
        q1 = request.form['q1']
        q2 = request.form['q2']
        q3 = request.form['q3']
        d = session["d"]
        d = list(d.items())
        cur.execute("SELECT answer, hint from QUESTIONS WHERE userid = %s and qid=%s", (session['id'], d[0][0]))
        row1 = cur.fetchall() #row = [('password')]
        row1 = list(itertools.chain(*row1))
        cur.execute("SELECT answer, hint from QUESTIONS WHERE userid = %s and qid=%s", (session['id'], d[1][0]))
        row2 = cur.fetchall() #row = [('password')]
        row2 = list(itertools.chain(*row2))
        cur.execute("SELECT answer, hint from QUESTIONS WHERE userid = %s and qid=%s", (session['id'], d[2][0]))
        row3 = cur.fetchall() #row = [('password')]
        row3 = list(itertools.chain(*row3))
        print(q1, q2, q3, row1, row2, row3)
        if q1 == row1[0] and q2 == row2[0] and q3 == row3[0]:
            return render_template("sample.html", msg="successful login")
        else:
            return render_template("sample.html", msg="wrong answers")

@app.route('/after-otp', methods=['GET', 'POST'])
def after_otp():
    if request.method == "POST":
        email = session['email']
        otp = session['otp']
        entered_otp = request.form['otp']
        print(otp, entered_otp, type(entered_otp), type(otp))
        if (otp == entered_otp):
            return redirect("/security-ques")
        return render_template("sample.html", msg="sent email to" + email)



@app.route('/registerUser', methods = ['POST'])
def registerCustomer():
    if request.method == 'POST':
        cfname = request.form['cfname']
        clname = request.form['clname']
        cphone = request.form['cphone']
        cuname = request.form['cuname']
        cemail = request.form['cemail']
        cpassword = request.form['cpassword']
        q1 = request.form['q1']
        q2 = request.form['q2']
        q3 = request.form['q3']
        q4 = request.form['q4']
        q5 = request.form['q5']
        hq1 = request.form['hq1']
        hq2 = request.form['hq2']
        hq3 = request.form['hq3']
        hq4 = request.form['hq4']
        hq5 = request.form['hq5']

        #Find out ID
        cur.execute("SELECT COUNT(*) FROM USERS;")
        row = cur.fetchall()
        row1 = list(itertools.chain(*row))
        cid = row1[0] + 1
        print(cid, cfname)
        #session['id'] = cid
        cur.execute("SELECT phonenumber, email from USERS")
        cpe = cur.fetchall()
        c_ph = [''.join(i[0]) for i in cpe]
        c_mail = [''.join(i[1]) for i in cpe]
        print("reg customer", c_ph, c_mail, cphone, cemail)
        if cphone not in c_ph and cemail not in c_mail: 
            cur.execute("INSERT INTO USERS VALUES(%s, %s, %s, %s, %s, %s, %s);", (cid, cuname, cpassword, cfname, clname, cphone, cemail))
            cur.execute("INSERT INTO QUESTIONS VALUES(%s, %s, %s, %s)", (cid, 1, q1, hq1))
            cur.execute("INSERT INTO QUESTIONS VALUES(%s, %s, %s, %s)", (cid, 2, q2, hq2))
            cur.execute("INSERT INTO QUESTIONS VALUES(%s, %s, %s, %s)", (cid, 3, q3, hq3))
            cur.execute("INSERT INTO QUESTIONS VALUES(%s, %s, %s, %s)", (cid, 4, q4, hq4))
            cur.execute("INSERT INTO QUESTIONS VALUES(%s, %s, %s, %s)", (cid, 5, q5, hq5))

            db.commit()
            return render_template("login.html", msg="login to continue")
        else:
            return render_template("error.html", error="email/phone number already exists!")

@app.route('/after-login', methods=['POST'])
def after_login():
    if request.method == "POST":
        uname = request.form['cuname']
        pswd = request.form['cpassword']
        print(pswd, uname)
        #Customer Validation
        cur.execute("SELECT email, userid, pswd from USERS WHERE username = %s", (uname, ))
        row = cur.fetchall() #row = [('password')]
        row = list(itertools.chain(*row))
        print(row[2], pswd, type(row[0]), type(pswd))
        if row[2] == pswd:
                session['id'] = row[1]
                session['email'] = row[0]
                email = session['email']
                print(email)
                otp = generateOtp()
                session['otp'] = otp
                send_email(email, otp)
                return render_template("otp.html", msg="sent email to " + email)
                return redirect("/otp") #changed
        print("incorrect")
        return render_template("login.html", msg="Incorrect password!!")
        

if __name__ == "__main__":
    app.secret_key = 'secret'
    app.run(host='127.0.0.1', debug=True)
