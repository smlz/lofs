
class List(object):
    def __init__(self, first, rest=None):
        if rest is None:
            rest = Nil
        assert(isinstance(rest, List))
        self.first = first
        self.rest = rest

    def cons(self, el):
        return List(el, self)

    def append(self, el):
        if self is Nil:
            return List(el)
        else:
            rest = self.rest.append(el)
            return List(self.first, rest)
            
    def __iter__(self):
        l = self
        while l is not Nil:
            yield l.first
            l = l.rest

    def __getitem__(self, index):
        if index == 0:
            return self.first
        else:
            return self.rest[index - 1]
        
    def __str__(self):
        if self.first and self.first == 'func':
            self = list(self)[0:-1]
        return '(' + ' '.join(str(x) for x in self) + ')'
    def __repr__(self):
        return self.__str__()

class _Nil(List):
    def __init__(self):
        self.first = None
        self.rest = None

Nil = _Nil()


def tokenize(program):
    return program.replace('(', ' ( ').replace(')', ' ) ').split()


def parse(tokens):
    token = tokens.pop(0)   # Hohl das erste Element
    if token == '(':
        L = Nil
        while tokens[0] != ')':
            L = L.append(parse(tokens))
            #L.append(parse(tokens))
        tokens.pop(0)
        return L
    else:
        return atom(token)

def atom(token):
    try:
        return int(token)
    except:
        try:
            return float(token)
        except:
            return token

class Env(dict):
    def __init__(self, params=(), args=(), outer=None):
        self.update(zip(params, args))
        self.outer = outer
    def __getitem__(self, var):
        if var in self:
            return super(Env, self).__getitem__(var)
        elif self.outer:
            return self.outer[var]
        else:
            raise NameError("name '%s' is not defined" % var)

    def __str__(self):
        return "{\n" +  "\n".join('  %4s: %s' % (key, val) for key, val in self.items()) + "\n}"

    def __repr__(self):
        return self.__str__()

class Inner(object):
    def __init__(self, func):
        self.func = func
    def __call__(self, *args):
        return self.func(*args)
    def __str__(self):
        import itertools
        return "(func (%s) <built-in-function>)" % \
               " ".join(itertools.islice(self.func.__code__.co_varnames,
                                  self.func.__code__.co_argcount))
    def __repr__(self):
        return self.__str__()
    
def lispize(func):
    return Inner(func)

@lispize
def add(a, b):
    return a + b
@lispize
def sub(a, b):
    return a - b
@lispize
def mult(a, b):
    return a * b
@lispize
def div(a, b):
    return a / b
@lispize
def floordiv(a, b):
    return a // b
@lispize
def do(*args):
    return args[-1]

global_env = Env()
global_env.update({
    '+': add,
    '-': sub,
    '*': mult,
    '/': div,
    '//': floordiv,
    'do': do,
    '%': lispize(lambda a, b: a % b),
    '=': lispize(lambda a, b: a == b),
})

def apply(func, args):
    if isinstance(func, List):
        (_, params, body, env) = func
        return eval(body, Env(params, args, env))
    else:
        return func(*list(args))

def eval(x, env=global_env):
    if isinstance(x, (int, float)):    # Numbers
        return x
    elif isinstance(x, str):           # Operator
        return env[x]
    elif x.first == 'define':           # (define var exp)
        (_, var, exp) = x
        env[var] = eval(exp, env)
    elif x.first == 'func':             # (func (var...) body)
        # Eigentlich müsste das aktuelle env hier der Funktion übergeben werden
        (_, params, body) = x
        return x.append(env)
    elif x.first == 'if':
        (_, test, conseq, alt) = x
        return eval(conseq, env) if eval(test, env) else eval(alt, env)
    else:
        func = eval(x.first, env)
        args = Nil
        for exp in x.rest:
            args = args.append(eval(exp, env))
        return apply(func, args)
    
res = eval(parse(tokenize('''
(do
 (define gcd (func (a b) (if (= b 0) a (gcd b (% a b)))))
 (gcd 24 42)
)
''')))
