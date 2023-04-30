def sanitize(expression: str):
    return "".join(expression.split()).lower()

def tokensAsString(tokens: list):
    return "".join(x[1] for x in tokens)

def print_tree(node):
    stack = [(node, '')]
    while stack:
        current_node, indent = stack.pop()
        print(indent + current_node.value)
        stack.extend((child, indent + '  ') for child in current_node.children)