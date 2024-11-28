import asyncio

from flask import Flask
from flask import render_template, request

from prisma import Prisma
from prisma.models import Admin

app = Flask(__name__)

prisma = Prisma(auto_register=True)

async def handler_login(login, password):
    await prisma.connect()
    admin = await Admin.prisma().find_first(
        where={
            'login': login,
            'password': password,
        },
    )
    print("admin: ", admin)
    await prisma.disconnect()
    return admin

@app.route('/', methods=['post', 'get'])
def hello_world():
    message = ''
    if request.method == 'POST':

        login = request.form.get('login')
        password = request.form.get('password')

        admin = asyncio.run(handler_login(login, password))

        if  admin != None:
            message = "Вошли"
        else:
            message = "Не вошли"

    return render_template('index.html', message=message)

if __name__ == '__main__':
    # asyncio.run(app.run())
    app.run()
