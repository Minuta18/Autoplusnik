from flask import Flask, redirect, render_template
import Plusnik

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.args.get('action')
        klass = request.args.get('klass')

        if action != None and klass != None:
            if action == 'update':
                pass
            elif action == 'delete':
                pass
            elif action == 'create':
                pass
            elif action == 'edit':
                pass
        
        return redirect('/')
    return render_template(...) # TODO

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000) #