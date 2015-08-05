def tokenize(program):
    return program.replace('(', ' ( ').replace(')', ' ) ').split()


def parse(tokens):
    token = tokens.pop(0)   # Hohl das erste Element
    if token == '(':
        lst = []
        while tokens[0] != ')':
            lst.append(parse(tokens))
        tokens.pop(0)
        return lst
    else:
        try:
            return int(token)
        except:
            try:
                return float(token)
            except:
                return token

class Env(dict):
    def __init__(self, arg_names=(), args=(), outer=None):
        self.update(zip(arg_names, args))
        self.outer = outer

    # FIXME: besserer Name (find)
    def find(self, key):
        if key in self:
            return self[key]
        elif self.outer:
            return self.outer.find(key)
        else:
            raise NameError("Name '%s' is not defined." % key)

import operator as op
global_env = Env()
global_env.update({
    '+': op.add, '-': op.sub, '%': op.mod,
    '/': op.truediv, '//': op.floordiv,
    'do': lambda *args: args[-1],
    '>': op.gt,
    'true': True, 'false': False,
})

library = [
'(def < (fn (a b) (> b a)))',
'(def = (fn (a b) (if (< a b) false (if (< b a) false true))))',
'(def != (fn (a b) (if (= a b) false true)))',
'(def and (fn (a b) (if a b false)))',
'(def or (fn (a b) (if a true b) ))',
'(def not (fn a (if a false true)))',
'(def <= (fn (a b) (or (< a b) (= a b))))',
'(def =< <=)',
'(def >= (fn (a b) (not (< a b))))',
'(def => >=)',
'(def mul_acc (fn (a b res) (if (= a 0) res (mul_acc (- a 1) b (+ res b)))))', 
'(def * (fn (a b) (mul_acc a b 0)))',
]


def apply(func, args):
    if isinstance(func, list):
        # lispy function
        (arg_names, body, env) = func
        return evaluate(body, Env(arg_names, args, env))
    else:
        # Built-in function
        return func(*args)

global_env.update({'apply': apply})

def evaluate(expr, env=global_env):
    if isinstance(expr, (bool, int, float)):  # Literal bools and numbers
        return expr
    elif isinstance(expr, str):               # Defined value: get it!
        return env.find(expr)

    # Ok, expr must be a list then!

    if len(expr) == 0:
        return expr
    
    func = expr[0]
    args = expr[1:]

    # Special forms
    if func == 'def':
        (var, exp) = args
        result = evaluate(exp, env)
        env[var] = result
        return result
    elif func == 'fn':
        args.append(env)
        return args
    elif func == 'if':
        (test, conseq, altern) = args
        if evaluate(test, env):
            return evaluate(conseq, env)
        else:
            return evaluate(altern, env)
    else:
        # 'Normal' functions
        # Evaluate all values and then apply the arguments to the function
        func = evaluate(func, env)
        args = [evaluate(arg, env) for arg in args]
        return apply(func, args)


def interpret(program):
    tokens = tokenize(program)
    if tokens.count('(') != tokens.count(')'):
        raise Exception('Syntax Error: Unbalanced paranthesis')
    syntax_tree = parse(tokens)
    if len(tokens) > 0:
        raise Exception('Syntax Error: Could not parse entire program.')
    result = evaluate(syntax_tree)
    return result

for func in library:
    interpret(func)
    
print(interpret('''
(do
 (def gcd (fn (a b) (if (= b 0) a (gcd b (% a b)))))
 (gcd 24 42)
)
'''))

print(interpret(
    '((def gcd (fn (a b) (if (= b 0) a (gcd b (% a b))))) 24 42)'
))

print(interpret('(=> 2 1)'))

def repl(prompt='lispy> '):
    quit = False
    while not quit:
        try:
            prog = input(prompt)
            if prog == 'quit' or prog == 'exit':
                quit = True
            else:
                res = interpret(prog)
                print(res)
        except (KeyboardInterrupt, EOFError):
            quit = True
        except IndexError:
            print('Malformed expression (a.k.a. prarenthesis salad).')
        except Exception as e:
            print(e)
    print('Bye!')
    
if __name__ == '__main__':    
    repl()
