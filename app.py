from flask import Flask, render_template, request
from json import dumps
from time import time

app = Flask(__name__)

# users={'127.0.0.1':'Parasaran','1.1.1.1':'Test'}
# messages=[{'ip':'127.0.0.1','message':'Hello!'},{'ip':'1.1.1.1','message':'Hello from test!'}]
users={}
messages=[]

@app.route('/')
def homePage():
    return render_template('main.html',users=users,messages=messages,ip=request.remote_addr)

@app.route('/addUser',methods=['POST'])
def addNewUser():
    if request.remote_addr in users:
        return dumps({'status':False,'reason':'IP already exists'})
    else:
        users[request.remote_addr]=request.form['Alias']
        return dumps({'status':True,'reason':'User Added'})

@app.route('/send', methods=['POST'])
def send():
    messages.append({'ip':request.remote_addr,'message':request.form['message'],'timestamp':time()})
    return dumps({'status':'sent'})

@app.route('/receive')
def receive():
    pass


app.run(debug=True, port=3456)