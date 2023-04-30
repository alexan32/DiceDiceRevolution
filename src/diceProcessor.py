from tokenizer import *
from myParser import TreeGenerator
from interpreter import evaluateTree, treeToExpression

class DiceProcessor:

    def __init__(self):
        self.generator = TreeGenerator()

    def processDiceString(self, diceString:str, variables={}, advantage=""):
        
        total = None
        expression = ""

        # Step 1: tokenization
        tokens = tokenize(diceString)
        missingVars, tokens = replaceVariables(tokens, variables)
        if len(missingVars) > 0:
            raise Exception(f"Failed to populate the following variables: {[x[1] for x in missingVars]}")

        # Step 2: parsing
        root = self.generator.generateParseTree(tokens)
        
        # Step 3: interpreting
        total = evaluateTree(root, advantage)
        expression = treeToExpression(root)

        return total, expression
    

if __name__ == "__main__":
    dp = DiceProcessor()
    print(dp.processDiceString("10 / 3")[1])
    print(dp.processDiceString("1d20 + prof + dex", {"prof": "2", "dex": "3"}, advantage="")[1])
    print(dp.processDiceString("1d20 + prof + dex", {"prof": "2", "dex": "3"}, advantage="a")[1])
    print(dp.processDiceString("1d20 + prof + dex ", {"prof": "2", "dex": "3"}, advantage="d")[1])