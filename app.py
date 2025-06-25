from flask import Flask, render_template ,request , flash , redirect , url_for , session
import sqlite3

app = Flask(__name__, template_folder='./template')
app.secret_key="123"

con=sqlite3.connect("storage.db")
con.execute("create table if not exists customer(pid integer primary key,name text,contact integer,mail text,password text)")
con.close()

@app.route('/')
def hello():
    return render_template('hello.html')

@app.route('/login',methods = ["GET","POST"])
def login():
    if request.method == 'POST':
        mail = request.form['mail']
        password = request.form['password']
        con = sqlite3.connect("storage.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("select * from customer where mail=? and password=?",(mail,password))
        data = cur.fetchone()

        if data:
            session["mail"] = data["mail"]
            session["password"] = data["password"]
            return redirect("customer")
        else:
            flash("Email and Password Mismatch","danger")
    return redirect(url_for("hello"))

@app.route('/customer',methods=["GET" , "POST"])
def customer():
    return render_template("landing.html")

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        try:
            name=request.form['name']
            contact=request.form['contact']
            mail=request.form['mail']
            password=request.form['password']
            con=sqlite3.connect("storage.db")
            cur=con.cursor()
            cur.execute("insert into customer(name,contact,mail,password)values(?,?,?,?)",(name,contact,mail,password))
            con.commit()
            flash("Account Added  Successfully","success")
        except:
            flash("Error in Insert Operation","danger")
        finally:
            return redirect(url_for("hello"))
            con.close()

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("hello"))

if __name__ == '__main__':
    app.run(debug=True)
