from uuid import uuid4

class TreeNode:
    def __init__(self, value, _type):
        self.id = str(uuid4())
        self.value = value
        self.type = _type
        self.parent = None
        self.children = []
        self.data = {}
        

class TreeGenerator():

    def __init__(self):
        self.index = 0

    def generateParseTree(self, tokens):
        self.index = 0
        root = self.parseExpression(tokens)

        if self.index < len(tokens):
            raise SyntaxError("Invalid token: {}".format(tokens[self.index][1]))

        return root


    def parseExpression(self, tokens):
        # Parse the first term
        node = self.parseTerm(tokens)

        # Continue parsing while there are addition or subtraction tokens
        while self.index < len(tokens) and tokens[self.index][0] in ('ADD', 'SUB'):
            token = tokens[self.index]
            self.index += 1
            child = self.parseTerm(tokens)
            operatorNode = TreeNode(token[1], token[0])
            node.parent = operatorNode
            child.parent = operatorNode
            operatorNode.children.append(node)
            operatorNode.children.append(child)
            node = operatorNode

        return node


    def parseTerm(self, tokens):
        # Parse the first factor
        # node = self.parse_dice(tokens)
        node = self.parseFactor(tokens)

        # Continue parsing while there are multiplication or division tokens
        while self.index < len(tokens) and tokens[self.index][0] in ('MUL', 'DIV'):
            token = tokens[self.index]
            self.index += 1
            # child = self.parse_dice(tokens)
            child = self.parseFactor(tokens) 
            operatorNode = TreeNode(token[1], token[0])
            node.parent = operatorNode
            child.parent = operatorNode
            operatorNode.children.append(node)
            operatorNode.children.append(child)
            node = operatorNode

        return node

    def parseFactor(self, tokens):
        
        # Get the current token
        token = tokens[self.index]
        self.index += 1

        if token[0] in ('NUMBER', 'VAR', 'D'):

            # insert multiplication token of num followed immediately by paren
            if self.index < len(tokens) and tokens[self.index][0] == 'LPAREN':
                tokens.insert(self.index, ('MUL', '*'))

            # Create a leaf node with the token value (number or variable)
            return TreeNode(token[1], token[0])

        elif token[0] == 'LPAREN':
            # If the token is a left parenthesis, parse the expression inside the parentheses
            node = self.parseExpression(tokens)
            # Verify that there is a matching right parenthesis
            if tokens[self.index][0] != 'RPAREN':
                raise SyntaxError("Missing closing parenthesis")
            self.index += 1

            return node
        elif token[0] == 'SUB' and self.index < len(tokens) and tokens[self.index][0] == 'NUMBER':
            # Handling negative numbers (unary minus)
            numberToken = tokens[self.index]
            self.index += 1

            # Create a negative number node
            return TreeNode('-' + numberToken[1], numberToken[0])
        else:
            raise SyntaxError("Invalid token: {}".format(token[1]))