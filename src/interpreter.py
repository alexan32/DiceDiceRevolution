import re
from myDice import diceRoll

def evaluateTree(root, advantage=""):
    stack = []
    explored = []
    currentNode = root

    while currentNode != None:

        explored.append(currentNode.id)

        # get children of current node
        lchild = None
        rchild = None
        if len(currentNode.children) >= 1:
            lchild = currentNode.children[0]
        if len(currentNode.children) == 2:
            rchild = currentNode.children[1]

        # move to children if they have not yet been visited
        if lchild and lchild.id not in explored:
            currentNode = lchild
        elif rchild and rchild.id not in explored:
            currentNode = rchild
        
        # add value to stack. check for and perform operation. move to parent node.
        else:
            
            if currentNode.type == 'D':
                val = currentNode.value

                # use regex to split dice expression into operands and modifiers
                matchObject = re.match(r'(\d+)d(\d+)([A-Za-z0-9]*)',val)
                lop = matchObject.group(1)
                rop = matchObject.group(2)

                # evaluate dice expression
                dice, info = diceRoll(int(lop), int(rop), matchObject.group(3), advantage=advantage)
                currentNode.data["dice"] = dice
                currentNode.data["info"] = info
                total = sum(dice)

                # print(f"diceroll: {lop}D{rop} {dice} = {total}")
                stack.append(total)

            elif currentNode.type in ('ADD', 'SUB', 'MUL', 'DIV'):
                operator = currentNode.value
                rop = stack.pop(-1)
                lop = stack.pop(-1)
                # print(f"{lop} {operator} {rop}")
                result = eval(f"{lop} {operator} {rop}")
                stack.append(result)

            else:
                stack.append(currentNode.value)

            if currentNode.parent is None:
                if type(stack[0]) is float:
                    total = float('{0:.2f}'.format(stack[0]))
                    stack[0] = total
                currentNode.data["evaluation"] = stack
            currentNode = currentNode.parent

    return stack[0]


def treeToExpression(root):
    currentNode = root
    explored = []
    expression = ""

    while currentNode != None:

        # get children of current node
        lchild = None
        rchild = None
        if len(currentNode.children) >= 1:
            lchild = currentNode.children[0]
        if len(currentNode.children) == 2:
            rchild = currentNode.children[1]

        # 1. move to left child
        if lchild and lchild.id not in explored:
            currentNode = lchild
        
        # 2. if lc already explored, explore self
        elif currentNode.id not in explored:
            explored.append(currentNode.id)
            
            # update expression based on current node
            expression += currentNode.value
            if currentNode.type == 'D' and 'dice' in currentNode.data:
                expression += f"{currentNode.data['info']}({sum(currentNode.data['dice'])})"
        
        # 3. if lc and self explored, move to rc
        elif rchild and rchild.id not in explored:
            currentNode = rchild

        # 4. all children explored, move to parent
        else:
            
            # if tree already evaluated, add evaluation to expression
            if currentNode.parent is None and "evaluation" in currentNode.data:
                expression += f" = {currentNode.data['evaluation'][0]}"
            
            # move to parent
            currentNode = currentNode.parent

    for x in ["+", '-', '*', '/']:
        expression = f" {x} ".join(expression.split(x))

    return expression


if __name__ == "__main__":
    pass