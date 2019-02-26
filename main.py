import controller
from lib.config_loader import config as conf


def main():
    print('server is preparing..')
    app = controller.create_server()
    app.debug = conf.server.get('debug')
    app.run(host=conf.server.get('host'), port=conf.server.get('port'))
    print('server is ready')


if __name__ == '__main__':
    main()
