from threading import Thread
from time import sleep
import socket
import random
import json

password = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

logins_list = [
    'admin', 'Admin', 'admin1', 'admin2', 'admin3',
    'user1', 'user2', 'root', 'default', 'new_user',
    'some_user', 'new_admin', 'administrator',
    'Administrator', 'superuser', 'super', 'su', 'alex',
    'suser', 'rootuser', 'adminadmin', 'useruser',
    'superadmin', 'username', 'username1'
]

def logins():
    for login in logins_list:
        yield login

def random_password():
    '''function - generating random password of length from 6 to 10'''
    return ''.join(random.choice(password) for i in range(random.randint(6, 10)))

def random_login():
    return random.choice(list(logins()))

class Hacking():

    def __init__(self):
        self.ready = False
        self.sock = None
        self.serv = None
        self.connected = False
        self.message = []
        self.password = None
        self.login = None

    def start_server(self):
        self.serv = Thread(target=lambda: self.server())
        self.serv.start()
        self.ready = False
        while not self.ready:
            try:
                sleep(0.1)  # socket needs to be set up before test
            except KeyboardInterrupt:
                pass

    def stop_server(self):
        self.sock.close()
        self.serv.join()

    def server(self):
        '''function - creating a server and answering clients'''
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('localhost', 9090))
        self.ready = True
        print("Server listening on port 9090" )
        print("Server username: ", self.login )
        print("Server password: ", self.password )
        try:
            self.sock.listen(1)
            conn, addr = self.sock.accept()
            self.connected = True
            conn.settimeout(15)
            while True:
                data = conn.recv(1024)
                self.message.append(data.decode('utf8'))
                if len(self.message) > 1_000_000:
                    conn.send(
                        json.dumps({
                            'result': 'Too many attempts to connect!'
                        }).encode('utf8'))
                    break
                if not data:
                    break

                try:
                    login_ = json.loads(data.decode('utf8'))['login']
                    password_ = json.loads(data.decode('utf8'))['password']
                except:
                    conn.send(json.dumps({'result': 'Bad request!'}).encode('utf8'))
                    continue

                if login_ == self.login:
                    if self.password == password_:
                        conn.send(
                            json.dumps({
                                'result': 'Connection success!'
                            }).encode('utf8'))
                        break
                    elif self.password.startswith(password_):
                        conn.send(
                            json.dumps({
                                'result': 'Exception happened during login'
                            }).encode('utf8'))
                    else:
                        conn.send(
                            json.dumps({
                                'result': 'Wrong password!'
                            }).encode('utf8'))
                else:
                    conn.send(json.dumps({'result': 'Wrong login!'}).encode('utf8'))
            conn.close()
        except:
            pass

    def generate(self):
        self.message = []
        self.password = random_password()
        self.login = random_login()
        self.start_server()

test = Hacking()
test.generate()
