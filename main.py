from flask import Flask, render_template, session, request, redirect, url_for, abort
import os
from dotenv import load_dotenv
import json

load_dotenv()
if 'FLASK_SECRET_KEY' not in os.environ:
    raise Exception('Error: no FLASK_SECRET_KEY')

kv = json.load(open('kv.json'))

app = Flask(__name__, template_folder='templates')
app.secret_key = os.environ['FLASK_SECRET_KEY']


@app.route('/')
def index():
    return templates('')


@app.route('/<path:filename>')
def templates(filename: str):
    file_path = os.path.join('templates', filename)
    if not os.path.exists(file_path):
        abort(404)

    params = request.args
    if session.get('verified', False):
        if filename == '':
            return render_template('index.html')
        else:
            return render_template(filename)
    else:
        hash = params.get('hash', None)
        if hash is None:
            return render_template('403.html'), 403
        elif hash in kv:
            if not kv[hash]:
                kv[hash] = True
                json.dump(kv, open('kv.json', 'w'), indent=2)
                session['verified'] = True
                return redirect(url_for('index'))
            else:
                return render_template('403.html'), 403
        else:
            return render_template('403.html'), 403


@app.route('/api')
def api():
    if session.get('verified', False):
        return {'msg': 'ok'}
    else:
        return {'msg': '403'}, 403


if __name__ == '__main__':
    app.run(port=5002)
