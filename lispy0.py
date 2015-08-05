def tokenize(program):
    return program.replace('(', ' ( ').replace(')', ' ) ').split()


def parse_literal(token):
    try:
        return int(token)         # Versuche int zu parsen
    except:
        try:
            return float(token)   # Versuche float zu parsen
        except:
            return token          # Weder noch, also etwas definiertes (hoffentlich)


def parse(tokens):
    stapel = []
    aktuell = []
    for token in tokens:
        if token == '(':                           # Neue Liste anfangen
            stapel.append(aktuell)
            aktuell = []
        elif token == ')':                         # aktuelle Liste abschliessen
            fertig = aktuell
            aktuell = stapel.pop()
            aktuell.append(fertig)
        else:
            aktuell.append(parse_literal(token))

    if len(aktuell) != 1 or stapel != []:
        raise Exception("Parser error: Only single expressions are allowed.")

    return aktuell[0]

def add(a, b):
    return a + b

def sub(a, b):
    return a - b

global_env = dict()
global_env.update({
    '+': add, '-': sub
})

def apply(func, args):
    return func(*args)

def evaluate(expr):
    if isinstance(expr, (int, float)):  # Literal bools and numbers
        return expr
    else:
        func = expr[0]
        args = expr[1:]
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
