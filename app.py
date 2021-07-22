from flask import Flask, render_template, request
from json import dumps

app = Flask(__name__)

users={}
messages={}

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


app.run(debug=True, port=3456)