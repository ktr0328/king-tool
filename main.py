import controller
from lib.config_loader import config as conf


def main():
    app = controller.create_server()
    app.debug = conf.server.get('debug')
    app.run(host=conf.server.get('host'), port=conf.server.get('port'))


if __name__ == '__main__':
    main()
