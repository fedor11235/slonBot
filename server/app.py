import asyncio

from flask import Flask
from flask import render_template, request
from flask_login import LoginManager

from handlers.login import handler_login 

app = Flask(__name__)

# login = LoginManager(app)

@app.route('/login', methods=['post', 'get'])
def hello_world():
    message = ''
    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        admin = asyncio.run(handler_login(username, password))

        if  admin != None:
            message = "Вошли"
        else:
            message = "Не вошли"

    return render_template('login.html', message=message)

if __name__ == '__main__':
    app.run()
