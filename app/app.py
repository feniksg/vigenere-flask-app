from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from .utils import ( 
    get_users,
    process_login,
    is_token_alive,
    process_message,
    vigenere_encrypt,
    get_history
)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'MegasecretServerKey!!!'
socketio = SocketIO(app)

CONTEXT = {
    'title': 'Vigenere',
    'page_title': 'Дипломная работа <Вставить имя>'
}

USERS = get_users()

@app.route('/')
def index():
    return render_template('index.html', **CONTEXT)

@app.route('/chat')
def chat():
    return render_template('chat.html', **CONTEXT)

@socketio.on('history')
def history(data):
    history = get_history()
    for mes in history:
        mes['text'] = vigenere_encrypt(mes['text'], USERS[data['username']]['token'])
    emit('gethistory', {'history':history})


@socketio.on('usersendmessage')
def get_message(data):
    if data['type'] == 'login':
        data['sid'] = request.sid
        print('SID при логине:', request.sid)
        response = process_login(USERS, data)
        emit('login', response)
    elif data['type'] == 'check':
        token = data.get('token', None)
        if token:
            res = is_token_alive(USERS, token, request.sid)
        else:
            res = False
        emit('check', {'result': res})
    elif data['type'] == 'send':
        print(f'Получено зашифрованное сообщение от { data["username"] if data.get("username",None) else "Неизвестного пользователя" }')
        data = process_message(USERS, data)
        print('SID отправителя:', request.sid)
        for user in USERS.keys():
            sid = USERS[user].get('sid', None)
            if sid:
                response = {
                    'timestamp': data['timestamp'],
                    'username': data['username'],
                    'text': vigenere_encrypt(data['text'], USERS[user]['token'])
                }
                print('Отправляю сообщение на',sid)
                emit('getmessage', response, room=sid)




@socketio.on('message')
def handle_message(msg):
    print('Message: ' + msg)
    emit('message',msg)

if __name__ == '__main__':
    socketio.run(app, debug=True)
