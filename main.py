from flask import Flask,render_template, redirect,request, session
from datetime import datetime
import shutil
import os
from flask_sqlalchemy import SQLAlchemy
import csv
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt

logged='F'
log_uname = 'qwertyiooplkj'
cleared = 'F'
local_host = True


app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

app.secret_key='super-secret-key'
if (local_host):
    # app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/techbin"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///techbin.db"
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
    Points = db.Column(db.Integer, unique=False, nullable=True)
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
    global logged
    if ('user' in session and session['user']==log_uname):
        logged='T'
    return render_template("home.html", logged=logged, log_uname=log_uname)

@app.route('/about')
def about():
    global logged
    if ('user' in session and session['user']==log_uname):
        logged='T'
    return render_template("about.html", logged=logged, log_uname=log_uname)

@app.route('/contact')
def contact():
    global logged
    if ('user' in session and session['user']==log_uname):
        logged='T'
    return render_template("contact.html", logged=logged, log_uname=log_uname)

@app.route('/dashboard/<string:uname>')
def dashboard(uname):
    if ('user' in session and session['user']==log_uname and uname==log_uname):
        info = Garbage.query.filter_by(Uname=uname).first()
        name_info = Login.query.filter_by(Uname=uname).first()
        months = ['January','February','March','April','May','June','July','August','September','October','November','December']
        weights = [info.Jan,info.Feb,info.March,info.April,info.May,info.June,info.July,info.August,info.Sept,info.Oct,info.Nov,info.Decem]
        fig = plt.figure()
        plt.plot(months,weights)
        plt.xticks(rotation=90)
        for filename in os.listdir('./static/img'):
            rm_path = os.path.join('./static/img', filename)
            shutil.rmtree(rm_path)
        # shutil.rmtree('./static/img')
        now=datetime.now()
        current_time = now.strftime("%H%M%S")
        path = './static/img/img'+current_time+'/plot.png'
        mk_path = './static/img/img'+current_time
        os.mkdir(mk_path)
        plt.savefig(path, bbox_inches='tight')
        # plt.show()
        this_month = datetime.now().month
        prev_month = this_month-1
        return render_template("index.html", info=info, name_info=name_info, current_time=current_time, this_month=this_month, prev_month=prev_month)
    else:
        return redirect('/')

# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response

@app.route('/login', methods=['GET', 'POST'])
def login():
    global log_uname
    if ('user' in session and session['user']==log_uname):
        return redirect('/')
    page='login'
    u_w='F'
    p_w='F'
    if (request.method=='POST'):
        Uname=request.form.get('uname')
        password= request.form.get('pass')
        log_det = Login.query.filter_by(Uname=Uname).first()
        try:
            if (log_det.Uname==Uname and log_det.password==password):
                log_uname=Uname
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
    global logged
    if ('user' in session and session['user']==log_uname):
        logged='F'
        session.pop('user', None)
        return redirect('/')
    else:
        return redirect('/login')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if ('user' in session and session['user']==log_uname):
        return redirect('/')
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
            entry_garbage = Garbage(Uname=Uname, Bio=0, Non_Bio=0, E_waste=0, Jan=0, Feb=0, March=0, April=0, May=0, June=0, July=0, August=0, Sept=0, Oct=0, Nov=0, Decem=0)
            db.session.add(entry_garbage)
            db.session.add(entry_login)
            db.session.commit()
    # print(same_u)
    # print(same_e)
    return render_template("signup.html", same_u=same_u, same_e=same_e,page=page)


@app.route('/dashboard')
def o_dashboard():
    global log_uname
    if ('user' in session and session['user']==log_uname):
        t_api='/dashboard/'+log_uname
        return redirect(t_api)
    else:
        return redirect('/login')

@app.route('/upload/<string:uname>', methods=['POST'])
def upload(uname):
    if(request.method=='POST'):
        global cleared
        content = request.get_json()
        editable = Garbage.query.filter_by(Uname=uname).first()
        old_bio = editable.Bio
        old_non_bio = editable.Non_Bio
        old_e_waste = editable.E_waste
        present_hour = datetime.now().time().strftime("%H")
        present_min = datetime.now().time().strftime("%M")
        print(datetime.now().date().weekday())
        if (present_hour == 12 and present_min>=0 and present_min<=50):
            if(old_bio<1 and old_non_bio<1 and old_e_waste<1 and cleared=='F'):
                cleared = 'T'
                editable.Points = editable.Points + 5
                db.session.commit()
                return redirect('/')
        if (present_hour == 13):
            if (cleared == 'F'):
                editable.Points = editable.Points - 5
            cleared = 'F'
        editable.Bio = content['bio']
        editable.Non_Bio = content['non_bio']
        editable.E_waste = content['e_waste']
        if ((int(content['bio'])-int(old_bio)) > 0):
            new_point = int(editable.Points) + (int(content['bio'])-int(old_bio))
            editable.Points = new_point
        if ((int(content['non_bio'])-int(old_non_bio)) > 0):
            new_point = int(editable.Points) + (int(content['non_bio'])-int(old_non_bio))
            editable.Points = new_point
        if ((int(content['e_waste'])-int(old_e_waste)) > 0):
            new_point = int(editable.Points) + (int(content['e_waste'])-int(old_e_waste))
            editable.Points = new_point
        db.session.commit()
        return redirect('/dashboard')

app.run(host="0.0.0.0", port="1200", debug=True)