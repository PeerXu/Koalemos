import os
from flask import Flask
from flask import request

from koalemos import Koalemos

app = Flask('Koalemos')

@app.route('/', methods=['GET'])
@app.route('/puzzle', methods=['GET'])
def puzzle():
    k = Koalemos.get_instance()
    return '%s,%s,%s' % (k.S, k.X, k.N)

@app.route('/history', methods=['GET'])
def history():
    k = Koalemos.get_instance()
    n = int(request.args['n'] if 'n' in request.args else 5)
    n = n if n < len(k.HISTORY) else len(k.HISTORY)
    history = k.HISTORY[-n:]
    output = '\n'.join([','.join(map(str, record)) for record in history])
    return output, 200

@app.route('/commit', methods=['POST'])
def commit():
    if 'r' not in request.form:
        return 'require param: r', 400

    r = request.form['r']
    if len(r) < 1 or len(r) > 40:
        return 'len(r) between [1, 40]', 400

    k = Koalemos.get_instance()
    if not all([x in k.CHARSET for x in r]):
        return 'all charset in r must in [0-9a-f]', 400

    if k.match(r):
        return '', 204
    else:
        return 'verify failed', 400

def main():
    host = os.environ.get('KOALEMOS_HOST', '0.0.0.0')
    port = int(os.environ.get('KOALEMOS_PORT', 51209))
    debug = os.environ.get('KOALEMOS_DEBUG', 'true').lower() in ('true', '1')
    print 'koalemos server listen on %s:%s, debug=%s' % (host, port, 'on' if debug else 'off')
    app.run(host=host, port=port, debug=debug)
