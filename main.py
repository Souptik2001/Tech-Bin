from flask import Flask,render_template, redirect,request, session
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
    email = db.Column(db.String(80), unique=True, nullable=False)
    address = db.Column(db.String(80), unique=True, nullable=False)
    ph_no = db.Column(db.String(80), unique=True, nullable=False)
    Name = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)



@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    page='login'
    u_w='F'
    p_w='F'
    if (request.method=='POST'):
        Uname=request.form.get('uname')
        password= request.form.get('pass')
        log_det = Login.query.filter_by(Uname=Uname).first()
        try:
            if (log_det.Uname==Uname and log_det.password==password):
                session['user']=Uname
            else:
                p_w='T'
                return render_template("login.html", p_w=p_w,page=page)
        except:
            u_w='T'
            return render_template("login.html", u_w=u_w,p_w=p_w,page=page)
        return redirect('/')
    return render_template("login.html", u_w=u_w,p_w=p_w,page=page)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@app.route('/signup', methods=['GET','POST'])
def signup():
    page='signup'
    same_u='F'
    same_e='F'
    if (request.method=='POST'):
        Uname = request.form.get('uname')
        Name = request.form.get('name')
        address = request.form.get('address')
        email = request.form.get('email')
        ph_no = request.form.get('ph_no')
        password = request.form.get('pass')
        duplicate_u = Login.query.filter_by(Uname=Uname).first()
        duplicate_e = Login.query.filter_by(email=email).first()
        # print(duplicate.Uname)
        try:
            try:
                if (duplicate_e.email==email):
                    same_e = 'T'
                    return render_template("signup.html", same_u=same_u, same_e=same_e,page=page)
            except:
                if (duplicate_u.Uname==Uname):
                    same_u = 'T'
                    return render_template("signup.html", same_u=same_u, same_e=same_e,page=page)
        except:
            entry_login = Login(Uname=Uname, Name=Name, password=password, email=email, address=address, ph_no=ph_no)
            entry_garbage = Garbage(Uname=Uname)
            db.session.add(entry_garbage)
            db.session.add(entry_login)
            db.session.commit()
    # print(same_u)
    # print(same_e)
    return render_template("signup.html", same_u=same_u, same_e=same_e,page=page)

app.run(debug=True)