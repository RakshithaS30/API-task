import json
from flask import Flask,session,render_template,request,redirect,url_for,jsonify
import requests
from apscheduler.schedulers.background import BackgroundScheduler

app=Flask(__name__)
def get_weather():
    requests.get("http://127.0.0.1:5000/weather?page=1")
    requests.get("http://127.0.0.1:5000/weather?page=2")
    requests.get("http://127.0.0.1:5000/weather?page=3")
    
scheduler =BackgroundScheduler()
job = scheduler.add_job(get_weather,'interval',minutes=30)
scheduler.start()

app.secret_key='asdsdfsdfs13sdf_df%&'

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        valid_email="admin@gmail.com"
        valid_password="admin"
        if (request.form['email']==valid_email and request.form['password']==valid_password):
            session['email']=request.form['email']
            session['password']=request.form['password']
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email',None)
    session.pop('password',None)
    return redirect(url_for('index'))

@app.route('/weather')
def weather():
    API_KEY = 'f30a6195250f293d53c6d4ec53eae69a'  
    url=''
    print(request.args.get("page"))
    if (request.args.get("page")=='1'):
        url = f'http://api.openweathermap.org/data/2.5/group?id=524901,703448,2643743,5128581,4068590,4068590,5308655,4119403,5389519,2643741&APPID={API_KEY}'
    elif (request.args.get("page")=='2'):
        url = f'http://api.openweathermap.org/data/2.5/group?id=4174757,4553440,4281730,5412347,5325738,5150529,5323810,5392900,5387890,5505411&APPID={API_KEY}'
    elif (request.args.get("page")=='3'):
        url = f'http://api.openweathermap.org/data/2.5/group?id=149653,149658,149703,149768,149775,149792,149812,149854,149876,149879&APPID={API_KEY}'
    else:
        print('NOT POSSIBLE')
   
    response = requests.get(url).json()
    results = []
    #print(response)
    cities=response['list']
    for city in cities:
        print("City Name\t"+city['name'])
        print("Temperature\t"+str(city['main']['temp']))
        print("Humidity\t"+str(city['main']['humidity']))
        print("Pressure\t"+str(city['main']['pressure']))
        print()
        results.append(
            {
                "city":city['name'],
                "temperature": city['main']['temp'],
                "humidity" :city['main']['humidity'],
                "pressure":city['main']['pressure'],
            }
        )
   
    #return redirect(url_for('index'))
    return jsonify({
        "pagination": request.args.get("page"),
        "list" : results
    })

@app.route('/')
def index():
    login=False
    if 'email' in session:
        login=True

    return render_template('/login_home.html',login=login)

if __name__=='__main__':
    app.run(debug=True)