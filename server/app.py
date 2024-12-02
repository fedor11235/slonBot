import asyncio

from flask import Flask, redirect, url_for
from flask import render_template, request
from flask_login import LoginManager

from handlers.common import handler_login, handler_create_suggestions, handler_get_suggestions

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

@app.route('/', methods=['post', 'get'])
def main_page():
    if request.method == 'POST':
        username = request.form.get('username')
        retail_price = request.form.get('retailPrice')
        wholesale_price = request.form.get('wholesalePrice')
        min_seats = request.form.get('minSeats')
        max_seats = request.form.get('maxSeats')
        details = request.form.get('details')
        date = request.form.get('date')
        time = request.form.get('time')
        asyncio.run(handler_create_suggestions(
            username=username,
            retail_price=retail_price,
            wholesale_price=wholesale_price,
            min_seats=min_seats,
            max_seats=max_seats,
            details=details,
            date=date,
            time=time
        ))

    return render_template('suggestions_create.html', page="create")

@app.route('/list', methods=['get'])
def list_page():
    suggestions = asyncio.run(handler_get_suggestions())
    return render_template('suggestions_list.html', page="list", suggestions=suggestions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3002)
