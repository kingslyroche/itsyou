from flask import Flask , request , render_template,session
from flask_sqlalchemy import SQLAlchemy
import requests
import datetime
import os


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') 
app.permanent_session_lifetime = datetime.timedelta(days=365)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

api_key=os.getenv('IPSTACK_API')

db = SQLAlchemy(app)

class itsyou(db.Model):
   id = db.Column(db.Integer(), primary_key=True)
   ip = db.Column(db.String(255), nullable=False)
   region = db.Column(db.String(255), nullable=False)
   browser = db.Column(db.String(255), nullable=False)
   version = db.Column(db.String(255), nullable=False)
   platform = db.Column(db.String(255), nullable=False)
   date = db.Column(db.DateTime(), default=datetime.datetime.utcnow)




@app.route("/", methods=["GET"])
def index():
    session.permanent = True
    
    if not request.headers.getlist("X-Forwarded-For"):
        ip = request.remote_addr
    else:
        ip = request.headers.getlist("X-Forwarded-For")[0]
    browser = request.user_agent.browser
    version = request.user_agent.version
    platform = request.user_agent.platform

    url = f'http://api.ipstack.com/{ip}?access_key={api_key}&format=1'
    api_data = requests.get(url).json()
    
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1
        
    else:
        session['visits'] = 1 # setting session data
    

    x={
        'ip': ip ,
        'region' : api_data['region_name'],
        'browser' : browser.title() ,
        'version' : version ,
        'platform' : platform.title(),
        'visits' : session.get('visits')
     }
    
    new_obj= itsyou(ip= str(ip),region=str(x['region']),browser=str(browser),version=str(version),platform=str(platform))
    db.session.add(new_obj)
    db.session.commit()
    


    return render_template("itsyou.html" , data = x)	




