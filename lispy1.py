from lispy0 import tokenize, parse, global_env, apply, repl

def mult(a, b):
    return a * b

def do(*args):
    if args:
        return args[-1]
    else:
        return []

global_env.update({
    '*': mult,
    'do': do,
})

def apply(func, args):
    return func(*args)

def evaluate(expr):
    if isinstance(expr, (int, float)):  # Literal bools and numbers
        return expr
    elif isinstance(expr, str):
        return global_env[expr]
    
    func = expr[0]
    args = expr[1:]
    
    if func == 'def':
        (var, exp) = args
        result = evaluate(exp)
        global_env[var] = result
    else:
        func = global_env[func]
        args = [evaluate(arg) for arg in args]
        return apply(func, args)


def interpret(program):
    tokens = tokenize(program)
    if tokens.count('(') != tokens.count(')'):
        raise Exception('Syntax Error: Unbalanced paranthesis')
    syntax_tree = parse(tokens)
    result = evaluate(syntax_tree)
    return result

print(interpret("""
(do
    (def pi 3.1459)
    (def r 1.5)
    (def circ (* pi (* 2 r)))
    circ
)
"""))

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
        except KeyError as e:
            print('KeyError: "%s" is not defined.' % e)
        except Exception as e:
            print(e)
    print('Bye!')
    
if __name__ == '__main__':    
    repl()
