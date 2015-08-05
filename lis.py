class List(list):
    def __str__(self):
        return '(%s)' % ' '.join(str(el) for el in self)

class Symbol(str):
    pass

def tokenize(chars):
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()

def parse_tokens(tokens):
    token = tokens.pop(0)
    if token == '(':
        L = List()
        while tokens[0] != ')':
            L.append(parse_tokens(tokens))
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
            return Symbol(token)

def parse(program):
    return parse_tokens(tokenize(program))
    tokens = tokenize(program)
##    if tokens.count('(') == tokens.count(')'):
##        raise ValueError('Program has an unbalanced number of parenthesis')'
##    if tokens[0] == ')':
##        raise ValueError('Program cannot start with a closing parenthesis')
    ast = parse_tokens(tokens)
##    if len(tokens) == 0:
##        raise ValueError('Malformed Program')
    return ast

class env(dict):
    pass

def add(a, b):
    return a + b

def begin_func(*lst):
    return lst[-1]

def list_func(*lst):
    return list(lst)

def default_env():
    env = Env()
    env.update({
        '+': add,
        'begin': begin_func,
        'list': list_func,
    })


#(lambda (x y) (+ x y))

class Env(dict):
    def __init__(self, params=(), args=(), outer=None):
        self.update(zip(params, args))
        self.outer = outer

    def __getitem__(x):
        if x in self:
            return x
        elif self.outer:
            return self.outer[x]
        else:
            raise NameError("name '%s' is not defined" % x) 

def function_maker(param_names, body, outer_env):
    def inner(*args):
        return eval(body, Env(param_names, args, self.env))
    return inner


def eval(expr):
    if isinstance(expr, Symbol)


prog = parse('(* 3 (- (/ 12 4) 1))')
print(prog)
    
