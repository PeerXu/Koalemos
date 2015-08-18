import time
from sha import sha as _sha

class Koalemos(object):
    _INSTANCE = None
    CHARSET = '0123456789abcdef'
    VERSION = '0.0.1'
    _VERBOSE = False

    def __init__(self, S='0'*40, X='0', N=1, HISTORY=None):
        self.S = S
        self.X = X
        self.N = N
        self.HISTORY = HISTORY if HISTORY else []
        self.fr = lambda s, r: s[:40 - len(r)] + r
        self.ff = lambda r: hex(int(r, 16)+1).strip('0x')
        self.sha = lambda s: _sha(s).hexdigest()

    def match(self, r):
        d = time.time()
        sr = self.fr(self.S, r)
        hsr = self.sha(sr)
        if hsr.count(self.X) >= self.N:
            self.HISTORY.append([len(self.HISTORY)+1, self.S, self.X, self.N, r, d])
            self.X, self.N = (lambda a: (self.CHARSET[a], self.N) if a < len(self.CHARSET) else (self.CHARSET[0], self.N+1))(self.CHARSET.index(self.X)+1)
            self.S = hsr
            return True
        else:
            return False

    def find(self, r=None):
        if r is None:
            r = 0

        while True:
            _r = hex(r)[2:]
            if self.match(_r):
                return _r
            r += 1

    @classmethod
    def get_instance(cls):
        if cls._INSTANCE is None:
            cls._INSTANCE = cls()
        return cls._INSTANCE
