from flask import Flask, render_template, request
from json import dumps
from time import time

app = Flask(__name__)

# users={'127.0.0.1':'Parasaran','1.1.1.1':'Test'}
# messages=[{'ip':'127.0.0.1','message':'Hello!'},{'ip':'1.1.1.1','message':'Hello from test!'}]
users = {}
messages = []


@app.route('/')
def homePage():
    m=0
    for i in messages:
        m=max(m,i['timestamp'])
    return render_template('main.html', users=users, messages=messages, ip=request.remote_addr,m=m)


@app.route('/addUser', methods=['POST'])
def addNewUser():
    if request.remote_addr in users:
        return dumps({'status': False, 'reason': 'IP already exists'})
    elif request.form['Alias'] in users or request.form['Alias'] == 'YOU':
        return dumps({'status': False, 'reason': 'Please enter some other name.'})
    else:
        users[request.remote_addr] = request.form['Alias']
        return dumps({'status': True, 'reason': 'User Added'})


@app.route('/send', methods=['POST'])
def send():
    messages.append({'ip': request.remote_addr,
                    'message': request.form['message'], 'timestamp': time()})
    return dumps({'status': 'sent'})


@app.route('/receive', methods=['POST'])
def receive():
    messages_to_return = []
    for i in messages:
        if float(request.form['timestamp']) < i['timestamp']:
            if request.remote_addr == i['ip']:
                messages_to_return.append(
                    {'sender': 'YOU', 'message': i['message'], 'timestamp': i['timestamp']})
            else:
                messages_to_return.append(
                    {'sender': users[i['ip']], 'message': i['message'], 'timestamp': i['timestamp']})
    return dumps(messages_to_return)

@app.route('/users', methods=['GET'])
def get_users():
    return dumps({'users':list(users.values())})


app.run(host='192.168.1.8', debug=True, port=3456)