import re
from util import sanitize

def tokenize(expression):
    tokenSpecification = [
        ('NUMBER',  r'(?<![d\d])\d+(?![d\d])(\.\d*)?'),                     # Integer or decimal number
        ('ADD',     r'\+'),                                                 # Addition operator
        ('SUB',     r'-'),                                                  # Subtraction operator
        ('MUL',     r'\*'),                                                 # Multiplication operator
        ('DIV',     r'/'),                                                  # Division operator
        ('POWER',   r'\^'),                                                 # Exponentiation operator
        ('LPAREN',  r'\('),                                                 # Left parenthesis
        ('RPAREN',  r'\)'),                                                 # Right parenthesis
        ('D',       r'\d+d\d+[A-Za-z0-9]*'),                                # Dice expression
        ('VAR',     r'(?<!\d)d?(?![\d])[a-zA-Z]+|[ace-zA-Z]+')              # Variable token
    ]
    tokenRegex = '|'.join('(?P<%s>%s)' % pair for pair in tokenSpecification)
    # Use regex to match tokens in the expression string
    return [(matchObject.lastgroup, matchObject.group()) for matchObject in re.finditer(tokenRegex, expression)]


def replaceVariables(tokens:list, variables:dict):
    i = 0
    missingVars = []
    while i < len(tokens):
        if tokens[i][0] == 'VAR':
            if tokens[i][1] in variables:
                newTokens = tokenize(sanitize(variables[tokens[i][1]])) 
                del tokens[i]
                tokens[i:i] = [('LPAREN', '(')] + newTokens + [('RPAREN', ')')]
            else:
                missingVars.append(tokens[i])
        i += 1
    return missingVars, tokens

if __name__ == '__main__':
    tokens = tokenize("2d20kh1 + 3(4/2) + prof + dex")
    missingVars, tokens = replaceVariables(tokens, {"prof": "7"})
    print(f"tokens: {tokens}")
    print(f"missing vars: {missingVars}")