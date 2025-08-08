"""
Filename: networking.py
Description: Defining Class Objects and Standard Objects for use in directory programs.
Author: Hunter R.
Date: 2025-08-05
"""

### Wrapper Function to log called function and report time performance and keyword arguments and positional arguments.
def my_logging(func):
    import time
    import logging
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        logging.info("Initializing {}() function.".format(func.__name__))
        logging.info(
            f"Finished running {func.__name__}() function with args={args}, kwargs={kwargs} "
            f"in {end_time - start_time:.5f} seconds."
        )
        return result
    return wrapper

class networkingDevice:
    def __init__(self, hostname='', username='', password='', device_type='cisco_ios', port='22'):
        self.hostname = hostname
        self._username = username
        self._password = password
        self.device_type = device_type
        self.port = port

    def __repr__(self):
        return (f"{self.__class__.__name__}(hostname={self.hostname!r}, "
                f"username={self._username!r}, password=****, "
                f"device_type={self.device_type!r}, port={self.port!r})")

    def __getitem__(self, item):
        if item == 'password':
            raise KeyError("Direct access to password is not allowed.")
        return self.get_connection_info().get(item)

    @property
    def password(self):
        raise AttributeError("Direct access to password is restricted.")

    @password.setter
    def password(self, password):
        raise AttributeError("Use: networkingDevice.set_password(password).")

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

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'password':
                self.set_password(value)
            elif key == 'username':
                self.set_user(value)
            elif key == 'hostname':
                self.set_host_ip(value)
            elif key == 'device_type':
                self.set_device_type(value)
            elif key == 'port':
                self.port = value


