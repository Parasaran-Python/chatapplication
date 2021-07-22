from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def homePage():
    return render_template('main.html')


app.run(debug=True, port=3456)