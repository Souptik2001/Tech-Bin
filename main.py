from flask import Flask,render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import csv
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt



local_host = True

app = Flask(__name__)
app.secret_key='super-secret-key'
if (local_host):
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/techbin"
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/techbin"
db = SQLAlchemy(app)
class Garbage(db.Model):
    sl_no = db.Column(db.Integer, primary_key=True)
    Uname = db.Column(db.String(80), unique=True, nullable=False)
    # Name = db.Column(db.String(80), unique=False, nullable=False)
    Bio = db.Column(db.Integer, unique=False, nullable=True)
    Non_Bio = db.Column(db.Integer, unique=False, nullable=True)
    E_waste = db.Column(db.Integer, unique=False, nullable=True)
    Jan = db.Column(db.Integer, unique=False, nullable=True)
    Feb = db.Column(db.Integer, unique=False, nullable=True)
    March = db.Column(db.Integer, unique=False, nullable=True)
    April = db.Column(db.Integer, unique=False, nullable=True)
    May = db.Column(db.Integer, unique=False, nullable=True)
    June = db.Column(db.Integer, unique=False, nullable=True)
    July = db.Column(db.Integer, unique=False, nullable=True)
    August = db.Column(db.Integer, unique=False, nullable=True)
    Sept = db.Column(db.Integer, unique=False, nullable=True)
    Oct = db.Column(db.Integer, unique=False, nullable=True)
    Nov = db.Column(db.Integer, unique=False, nullable=True)
    Decem = db.Column(db.Integer, unique=False, nullable=True)

class Login(db.Model):
    sl_no = db.Column(db.Integer, primary_key=True)
    Uname = db.Column(db.String(80), unique=True, nullable=False)
    Name = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)




@app.route('/dashboard/<string:uname>')
def dashboard(uname):
    info = Garbage.query.filter_by(Uname=uname).first()
    name_info = Login.query.filter_by(Uname=uname).first()
    months = ['January','February','March','April','May','June','July','August','September','October','November','December']
    weights = [info.Jan,info.Feb,info.March,info.April,info.May,info.June,info.July,info.August,info.Sept,info.Oct,info.Nov,info.Decem]
    fig = plt.figure()
    plt.plot(months,weights)
    plt.xticks(rotation=90)
    plt.savefig('static/img/plot.png', bbox_inches='tight')
    # plt.show()

    return render_template("index.html", info=info, name_info=name_info)

@app.route('/login')
def login():
    return render_template("login.html")

# @app.route('/signup')
# def signup():
#     uname = request.form.get('uname')
#     password = request.form.get('password')
#     user = Login.query.filter_by(Uname=uname).first()
#     if(uname==user.Uname and password==user.password):
#         session['user'] = 'uname'


@app.route('/signup')
def signup():
    Uname = request.form.get('uname')
    Name = request.form.get('name')
    password = request.form.get('password')
    entry_login = Login(Uname=Uname, Name=Name, password=password)
    entry_garbage = Garbage(Uname=Uname)
    db.session.add(entry_garbage)
    db.session.add(entry_login)
    db.session.commit()


app.run(debug=True)