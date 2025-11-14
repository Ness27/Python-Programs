"""
Filename: FortiGateAPI.py
Description: Creating a FortiGate API class.
Author: Hunter R.
Date: 2025-11-12
"""
import requests

class FortiGateAPI:
    def __init__(self, ip, headers, verify=False, proxies=None, disable_warnings=True, secure=True):
        self._secure=secure
        self.verify = verify
        self.ip = ip
        self.proxies=proxies

        if self._secure:
            self.url_prefix = 'https://' + self.ip
        else:
            self.url_prefix = 'http://' + self.ip

        if headers is None:
            self.headers = {}
        elif isinstance(headers, dict):
            self.headers = headers
        elif not isinstance(headers, dict):
            logging.info(f'Invalid headers type -> {type(headers)}. Use type dict.\n')
            self.headers = {}
        else:
            logging.info(f'Invalid headers type -> {type(headers)}. What Happened?! Error!\n')
            self.headers = {}

        if disable_warnings:
            requests.packages.urllib3.disable_warnings()

        authenticatedSession = requests.Session()
        authenticatedSession.post(self.url_prefix + '/logincheck', headers=self.headers, verify=self.verify)
        self.cookies = authenticatedSession.cookies

        for cookie in self.cookies:
            if cookie.name == "ccsrftoken":
                csrftoken = cookie.value[1:-1]  # token stored as a list
                self.headers['X-CSRFTOKEN'] = csrftoken

    def __enter__(self):
        return self

    def __del__(self):
        try:
            requests.post(self.url_prefix + '/logout', verify=self.verify, cookies=self.cookies, proxies=self.proxies)
        except AttributeError:
            print ("Looks like connection to "+self.ip+" has never been established")

    def __exit__(self, *args):
        pass

    def login(self, username, password):
        unpw = {'username': username, 'secretkey': password}

        # Might need to use
        # data='username=' + user + '&secretkey=' + password + '&ajax=1'

        altAuth = requests.post(self.url_prefix + '/logincheck',data=unpw, headers=self.headers, verify=self.verify)
        self.cookies = altAuth.cookies

        for cookie in self.cookies:
            if cookie.name == "ccsrftoken":
                csrftoken = cookie.value[1:-1]  # token stored as a list
                self.headers['X-CSRFTOKEN'] = csrftoken

    def get(self, path, api='v2', params=None):
        if isinstance(path, list):
            path = '/'.join(path) + '/'
        return requests.get(self.url_prefix + '/api/' + api + '/' + path, cookies=self.cookies, verify=self.verify, proxies=self.proxies, params=params)

    def put(self, path, api='v2', params=None, data=None):
        if isinstance(path, list):
            path = '/'.join(path) + '/'
        return requests.put(self.url_prefix + '/api/' + api + '/' + path, headers=self.headers,cookies=self.cookies,
                            verify=self.verify, proxies=self.proxies, params=params, json={'json': data})

    def post(self, path, api='v2', params=None, data=None, files=None):
        if isinstance(path, list):
            path = '/'.join(path) + '/'
        return requests.post(self.url_prefix + '/api/'+api+'/'+path, headers=self.header,cookies=self.cookies,
                            verify=self.verify, proxies=self.proxies, params=params, json={'json': data},
                            files=files)

    def delete(self, path, api='v2', params=None, data=None):
        if isinstance(path, list):
            path = '/'.join(path) + '/'
        return requests.delete(self.url_prefix + '/api/'+api+'/'+path, headers=self.header,cookies=self.cookies,
                            verify=self.verify, proxies=self.proxies, params=params, json={'json': data})

    def print_data(self, response):
        if response.status_code == 200:
            print(response.text)
        else:
            print('Response Code -> {}\n'.format(response.status_code))


