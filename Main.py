# Autoplusnik Copyright (C) 2023 Igor Samsonov

from website import app
from ConfigParser import Config

if __name__ == '__main__':
    conf = Config('./Config.yaml').config

    host = conf['web-site'].get('host') if conf['web-site'].get('host') != None else '0.0.0.0'
    port = conf['web-site'].get('port') if conf['web-site'].get('port') != None else '17500'
    
    debug_mode = conf.get('debug') if conf.get('debug') != None else True

    app.run(host=host, port=port, debug=debug_mode)