from flask import Flask , request , render_template,session
from flask_sqlalchemy import SQLAlchemy
import requests
import datetime



application=app = Flask(__name__)
app.secret_key = 'cC1YCIWOj9GgWspgNEo2' 
app.permanent_session_lifetime = datetime.timedelta(days=365)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@db_url:3306/db_name'


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
    
    ip = request.remote_addr
    browser = request.user_agent.browser
    version = request.user_agent.version
    platform = request.user_agent.platform
    
  
    
    
    
    
    url = 'http://api.ipstack.com/{}?access_key=01a41e65470ed1468e952ed82414e025&format=1'
    api_data = requests.get(url.format(ip)).json()
    
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



if __name__ == "__main__":
    app.run()



