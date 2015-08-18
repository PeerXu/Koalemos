from sha import sha as _sha
from flask import Flask
from flask import request

app = Flask('Koalemos')

CHARSET = '0123456789abcdef'

S = '0' * 40
X = '0'
N = 1

HISTORY = []

fr = lambda s, r: s[:40 - len(r)] + r
ff = lambda r: hex(int(r, 16)+1).strip('0x')
sha = lambda s: _sha(s).hexdigest()

def koalemos(r):
    global S, X, N

    sr = fr(S, r)
    hsr = sha(sr)
    if hsr.count(X) >= N:
        HISTORY.append([len(HISTORY)+1, S, X, N, r])
        X, N = (lambda a: CHARSET[a], N if a < len(CHARSET) else CHARSET[0], N+1)(CHARSET.index(X)+1)
        S = hsr
        return True
    else:
        return False

@app.route('/', methods=['GET'])
def index():
    return '%s,%s,%s' % (S, X, N)

@app.route('/history', methods=['GET'])
def history():
    n = request.args['n'] if 'n' in request.args else 5
    n = n if n < len(HISTORY) else len(HISTORY)
    history = HISTORY[n:]
    output = '\n'.join([map(str, record) for record in history])
    return output, 200

@app.route('/commit', methods=['POST'])
def commit():
    if 'r' not in request.form:
        return 'require param: r', 400
    r = request.form['r']
    if koalemos(r):
        return '', 204
    else:
        return 'verify failed', 400

app.run(host='0.0.0.0', port=9080, debug=True)
