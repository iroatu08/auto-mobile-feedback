from flask import Flask, render_template, request 
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate
from send_mail import send_mail
from collections.abc import Mapping

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config ['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:test007@localhost:5432/feedback'
    
else:
    app.debug = False
    app.config ['SQLALCHEMY_DATABASE_URI']='postgres://guncuhegbhtxax:04ca8b43b61151c4d58d4be006eaa6f2b6d9c8a15ba2c30fb16f903f3ff20b71@ec2-52-4-104-184.compute-1.amazonaws.com:5432/df6jlmv515q3pj'
    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
#db.create_all()

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200))
    email = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())
    
    def __init__(self, customer, email, dealer, rating, comments):
        self.customer= customer
        self.email=email
        self.dealer=dealer
        self.rating=rating
        self.comments = comments
        
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        email = request.form['email']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        
        if customer == '' or email =='':
            return render_template('index.html', message='please enter required fields')
        #print(customer, dealer, rating, comments)
        
        if db.session.query(Feedback).filter(Feedback.email==email).count() == 0:
            data = Feedback(customer, email, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(customer, email, dealer, rating, comments)
            return render_template('success.html')
        else:
         return render_template('index.html', message='you have already submitted!')
        

if __name__ == '__main__':
    app.run()
  