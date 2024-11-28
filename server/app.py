import asyncio

from flask import Flask, redirect, url_for
from flask import render_template, request
from flask_login import LoginManager

from handlers.login import handler_login 

app = Flask(__name__)

# login = LoginManager(app)

@app.route('/login', methods=['post', 'get'])
def login_page():
    message = ''
    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        admin = asyncio.run(handler_login(username, password))

        if  admin != None:
            message = "Вошли"
            return redirect(url_for('main_page'))
        else:
            message = "Не вошли"

    return render_template('login.html', message=message)

@app.route('/', methods=['get'])
def main_page():
    return render_template('suggestions_create.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3002)
