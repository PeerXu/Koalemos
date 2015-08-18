#!/usr/bin/env python
import sys
import time
from getopt import getopt
from getopt import GetoptError
from httplib import HTTPConnection
from urllib import urlencode

from koalemos import Koalemos

OPTIONS = {
    'host': '127.0.0.1',
    'port': 51209,
    'puzzles': 1,
    'verbose': False
}

def usage():
    sys.stderr.write('''usage: %s [OPTIONS]

Koalemos Client

Options:

    -h, --help                    dispaly usage
    -H, --host=127.0.0.1          Koalemos service address
    -P, --port=51209              Koalemos service port
    -n, --puzzles=1               solve how many puzzle, 0 is solve it untill
                                  the end of world.
    -V, --verbose                 display more detail
    -v, --version                 display version

''' % sys.argv[0])
    sys.exit(1)

def version():
    sys.stdout.write('''%s
''' % Koalemos.VERSION)
    sys.exit(0)

def parse_args():
    try:
        opts, args = getopt(sys.argv[1:], 'hvH:P:n:V', ['help', 'version', 'host=', 'port=', 'puzzles=', 'verbose'])
    except GetoptError as ex:
        sys.stderr.write(str(ex))
        usage()

    for k, v in opts:
        if k in ('-h', '--help'):
            usage()
        elif k in ('-v', '--version'):
            version()
        elif k in ('-H', '--host'):
            OPTIONS['host'] = v
        elif k in ('-P', '--port'):
            OPTIONS['port'] = int(v)
        elif k in ('-n', '--puzzles'):
            OPTIONS['puzzles'] = int(v)
        elif k in ('-V', '--verbose'):
            OPTIONS['verbose'] = True

def get_koalemos_status():
    conn = HTTPConnection(OPTIONS['host'], OPTIONS['port'])
    conn.request('GET', '/puzzle')
    res = conn.getresponse()
    if res.status != 200:
        sys.stderr.write('''[x] get koalemos status failed: %s, %s
''' % res.reason, res.read())
        sys.exit(2)

    dat = res.read()
    s, x, n = dat.split(',')
    return s, x, int(n)

def commit_koalemos(r):
    conn = HTTPConnection(OPTIONS['host'], OPTIONS['port'])
    conn.request('POST', '/commit',
                 body=urlencode({'r': r}),
                 headers={'Content-Type': 'application/x-www-form-urlencoded'})
    res = conn.getresponse()
    return (None, False) if res.status == 204 else (res.read(), True)

def main():
    parse_args()
    f = (lambda n: True) if (OPTIONS['puzzles'] == 0) else (lambda n: n < OPTIONS['puzzles'])
    cnt = 0
    while f(cnt):
        s, x, n = get_koalemos_status()
        begin = time.time()
        r = Koalemos(s, x, n).find()
        cost = time.time() - begin
        res, err = commit_koalemos(r)
        if not err:
            sys.stdout.write('''[i] %s: %s, %s, %s, %s, %s, %.6s
''' % (cnt+1, s, x, n, r, int(r, 16), cost))
            cnt += 1
        else:
            sys.stderr.write('''[x] commit failed: %s
''' % res)
