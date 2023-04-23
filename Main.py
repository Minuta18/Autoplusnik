from flask import Flask, redirect, render_template
import Plusnik
from ConfigParser import Config

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.args.get('action')
        klass = request.args.get('klass')

        if action != None and klass != None:
            if action == 'update':
                pass # TODO
            elif action == 'delete':
                pass
            elif action == 'create':
                pass
            elif action == 'edit':
                pass
        
        return redirect('/')
    return render_template(...) # TODO

if __name__ == '__main__':
    conf = Config('./Config.yaml').config

    host = conf['web-site'].get('host') if conf['web-site'].get('host') != None else '0.0.0.0'
    port = conf['web-site'].get('port') if conf['web-site'].get('port') != None else '17500'
    
    debug_mode = conf.get('debug') if conf.get('debug') != None else True

    app.run(host=host, port=port, debug=debug_mode)