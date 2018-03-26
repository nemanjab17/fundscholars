from flask import Flask, make_response, render_template, session, redirect, url_for, flash, request
import jinja2
import os

#---SQLAlchamy module imports---
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.exc import IntegrityError

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
my_loader = jinja2.ChoiceLoader([
        app.jinja_loader,
        jinja2.FileSystemLoader(['/home/nemanja/Documents/Development/fundfirm','/home/nemanja/Documents/Development/fundfirm/static','/home/nemanja/Documents/Development/fundfirm/static/img', '/home/nemanja/Documents/Development/fundfirm/templates']),])

db = SQLAlchemy(app)
app.jinja_loader = my_loader
#---CONFIG---
app.config['SECRET_KEY'] = 'ddwdwdasdwdfnjwdnjwdwudj'
#app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:alek@localhost/bookdb'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///'+basedir+'/data.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True



class Entry(db.Model):
    __tablename__='Users'
    id = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(64), unique=True, index=True)
    Country = db.Column(db.String(64))
    Date = db.Column(db.DateTime, nullable=False, default=datetime.now)

def post_to_db(obj):
    try:
        db.session.add(obj)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        print("Integrity error occured")

@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('home_eng'))

@app.route('/home-en', methods=['GET', 'POST'])
def home_eng():
    if request.method=='POST':
        country = request.form['country']
        email = request.form['email']
        obj = Entry(Email=email, Country=country)
        post_to_db(obj)
        print(country.encode(),email.encode())
        return redirect(url_for('home_eng'))
    return render_template('home-en.html')

@app.route('/home-rs', methods=['GET', 'POST'])
def home_rs():
    return render_template('home-rs.html')


db.create_all()
if __name__ == '__main__':
    app.run(debug=True)