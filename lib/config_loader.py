import yaml


class __Config(object):
    def __init__(self):
        with open('config.yml', 'r') as f:
            config = yaml.load(f)

            self.__service = config.get('service')
            self.__db = config.get('service').get('db')
            self.__server = config.get('service').get('server')
            self.__endpoint = config.get('kcg').get('get')
            self.__login = config.get('kcg').get('post').get('login')

    @property
    def service(self):
        return self.__service

    @property
    def db(self):
        return self.__db

    @property
    def server(self):
        return self.__server

    @property
    def endpoint(self):
        return self.__endpoint

    @property
    def login(self):
        return self.__login


config = __Config()
