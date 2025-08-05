"""
Filename: networking.py
Description: Defining Class Objects and Standard Objects for use in directory programs.
Author: Hunter R.
Date: 2025-08-05
"""

class networkingDevice():
    def __init__(self):
        self.hostname = ''
        self.username = ''
        self._password = ''
        self.device_type = 'cisco_ios'
        self.port = '22'

    def __getitem__(self, item):
        if item == 'password':
            raise KeyError("Direct access to password is not allowed.")
        return self.get_connection_info().get(item)

    def get_connection_info(self, include_password=False):
        info = {
            'host': self.hostname,
            'port': str(self.port),
            'device_type': self.device_type,
            'username': self.username,
        }
        if include_password is True:
            info['password'] = self._password
        return info

    def set_user(self, user = '<USER>'):
        self.username = user

    def set_password(self, password = '<PASSWORD>'):
        self._password = password

    def set_host_ip(self, ip):
        self.hostname = ip

    def set_device_type(self, device_type):
        self.device_type = device_type


if __name__ == "__main__":
    try:
        pass
    except KeyboardInterrupt:
        print('\nExiting: KeyboardInterrupt')
        exit(0)