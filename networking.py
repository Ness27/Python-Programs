"""
Filename: networking.py
Description: Defining Class Objects and Standard Objects for use in directory programs.
Author: Hunter R.
Date: 2025-08-05
"""

class networkingDevice:
    def __init__(self, hostname='', username='', password='', device_type='cisco_ios', port='22'):
        self.hostname = hostname
        self._username = username
        self._password = password
        self.device_type = device_type
        self.port = port

    def __repr__(self):
        return 'networkingDevice(hostname={}, username={}, password=****, device_type={}, port={})'.format(self.hostname,self._username, self.device_type, self.port)

    def __getitem__(self, item):
        if item == 'password':
            raise KeyError("Direct access to password is not allowed.")
        return self.get_connection_info().get(item)

    @property
    def password(self):
        raise AttributeError("Direct access to password is restricted.")

    @password.getter
    def password(self):
        raise AttributeError("Direct access to password is restricted.")

    def get_connection_info(self, include_password=False):
        info = {
            'host': self.hostname,
            'port': str(self.port),
            'device_type': self.device_type,
            'username': self._username,
        }
        if include_password == True:
            info['password'] = self._password
        return info

    def set_user(self, user = '<USER>'):
        self._username = user

    def set_password(self, password = '<PASSWORD>'):
        self._password = password

    def set_host_ip(self, ip):
        self.hostname = ip

    def set_device_type(self, device_type):
        self.device_type = device_type
