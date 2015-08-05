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

def parsee(tokens):
    token = tokens.pop(0)   # Hohl das erste Element
    if token == '(':
        lst = []
        while tokens[0] != ')':
            lst.append(parse(tokens))
        tokens.pop(0)
        return lst
    else:
        return parse_literal(token)

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

def interpret(program):
    tokens = tokenize(program)
    if tokens.count('(') != tokens.count(')'):
        raise Exception('Syntax Error: Unbalanced paranthesis')
    syntax_tree = parse(tokens)
    result = syntax_tree
    return repr(result)

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
