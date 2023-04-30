import re
from random import randint

# OPERATORS =========================================================

# mi
def minimum(rop:int, rolls:list, minimum:int):
    for i in range(len(rolls)):
        roll = rolls[i]
        if roll < minimum:
            while roll < minimum:
                roll = diceRoll(1, rop)[0][0]
            rolls[i] = roll
    return rolls, []

# ma
def maximum(rop:int, rolls:list, maximum:int):
    for i in range(len(rolls)):
        roll = rolls[i]
        if roll > maximum:
            while roll > maximum:
                roll = diceRoll(1, rop)[0][0]
            rolls[i] = roll
    return rolls, []

# rr
def reroll(rop:int, rolls:list, integer:int):
    dropped = []
    for i in range(len(rolls)):
        roll = rolls[i]
        if roll == integer:
            while roll == integer:
                dropped.append(roll)
                roll = diceRoll(1, rop)[0][0]
            rolls[i] = roll
    return rolls, dropped

# ro
def rerollOnce(rop:int, rolls:list, integer:int):
    dropped = []
    for i in range(len(rolls)):
        roll = rolls[i]
        if roll == integer:
            dropped.append(roll)
            rolls[i] = diceRoll(1, rop)[0][0]
    return rolls, dropped

# e
def explode(rop:int, rolls:list, integer:int):
    for roll in rolls:
        if roll == integer:
            rolls.append(diceRoll(1, rop)[0][0])
    return rolls

# k
def keep(rolls:list, selector:str, integer:int):
    if selector not in ('l', 'h', '<', '>'):
        raise TypeError(f"Invalid selector \"{selector}\". Valid selctors are l, h, <, and >.")
    kept = selectors[selector](rolls, integer)
    dropped = list(rolls)
    for x in kept:
        dropped.remove(x)
    return kept, dropped

# p
def drop(rolls:list, selector:str, integer:int):
    toDrop, toKeep = keep(rolls, selector, integer)
    return toKeep, toDrop

# SELECTORS==========================================================

# hX
def highest(rolls:list, quantity:int):
    rolls.sort()
    return rolls[len(rolls)-quantity:]

# lX
def lowest(rolls:list, quantity:int):
    rolls.sort()
    return rolls[:quantity]

# >X
def greaterThan(rolls:list, integer:int):
    return [x for x in rolls if x > integer]
    
# <X
def lessThan(rolls:list, integer:int):
    return [x for x in rolls if x < integer]

selectors = {
    'h': highest,
    'l': lowest,
    '<': lessThan,
    '>': greaterThan
}


# lop: left operand of the 'd' operator
# rop: right operand of the 'd' operator
# modifiers: rules applied after initial dice rolls
# peekSymbol: in dice results, marks that a di rolled its highest possible value
# removedSymbol: in dice rsults, marks that a di roll was removed from the di pool
# advantage: accepted values are "a", "d", or empty string
def diceRoll(lop:int, rop:int, modifiers:str="", peekSymbol:str="!", removedSymbol:str="~", advantage:str=""):
    rolls = []
    dropped = []

    if advantage not in ("a", "d", ""):
        raise ValueError(f"Invalid \"advantage\" arg for diceRoll fuction: {advantage}. valid values are \"a\", \"d\", or empty string.")
    elif advantage == "a" and lop == 1 and rop == 20 and modifiers == "":
        lop = 2
        modifiers = "kh1"
    elif advantage == "d":
        lop = 2
        modifiers = "ph1"

    for x in range(0, lop):
        rolls.append(randint(1, rop))
    # print(f"{lop}D{rop}={rolls}")


    if modifiers:

        # check for invalid characters
        match = re.match(r'((k|p|rr|ro|e|mi|ma)(\d+|h\d+|l\d+|\<\d+|\>\d+))*', modifiers)
        if match and match[0] != modifiers:
            badCharacters = modifiers.split(match[0])
            badCharacters.remove("")
            raise SyntaxError(f"Invalid character(s) in dice modifier expression '{lop}d{rop}{modifiers}': {badCharacters}")

        # loop over operation + selector combos
        dropped = []
        for match in re.findall(r'(k|p|rr|ro|e|mi|ma)(\d+|h\d+|l\d+|\<\d+|\>\d+)', modifiers):
            op = match[0]
            removed = []
            # print(match)

            # keep selection
            if op == 'k':
                if match[1].isdigit():
                    raise SyntaxError(f"invalid selector for 'keep' operation: {match[1]}")
                rolls, removed = keep(rolls, match[1][0], int(match[1][1:]))
            
            # drop selection
            elif op == 'p':
                if match[1].isdigit():
                    raise SyntaxError(f"invalid selector for 'drop' operation: {match[1]}")
                rolls, removed = drop(rolls, match[1][0], int(match[1][1:]))
            
            # reroll on X
            elif op == 'rr':
                if not match[1].isdigit():
                    raise SyntaxError(f"invalid selector for 'reroll' operation: {match[1]}")
                rolls, removed = reroll(rop, rolls, int(match[1]))
            
            # reroll once on X or reroll once on selection
            elif op == 'ro':
                if match[1].isdigit():
                    rolls, removed = reroll(rop, rolls, int(match[1]))
                else:
                    selection = selectors[match[1][0]](rolls, int(match[1][1:]))
                    removed = []
                    for roll in selection:
                        removed.append(roll.index(roll))
                        rolls[rolls.index(roll)] = diceRoll(1, rop)[0]
            
            # explode on X
            elif op == 'e':
                if not match[1].isdigit():
                    raise SyntaxError(f"invalid selector for 'explode' operation: {match[1]}")
                rolls = explode(rop, rolls, int(match[1]))
            
            # minimum X
            elif op == 'mi':
                if not match[1].isdigit():
                    raise SyntaxError(f"invalid selector for 'minimum' operation: {match[1]}")
                rolls, removed = minimum(rop, rolls, int(match[1]))
            
            # maximum X
            elif op == 'ma':
                if not match[1].isdigit():
                    raise SyntaxError(f"invalid selector for 'maximum' operation: {match[1]}")
                rolls, removed = maximum(rop, rolls, int(match[1]))

            dropped.extend(removed)

    isMaxPipe = lambda x: f"{peekSymbol}{x}" if x == rop else str(x)
    info = [f"{removedSymbol}{x}" for x in dropped] + [isMaxPipe(x) for x in rolls]

    return rolls, info


if __name__ == "__main__":
    rolls, info = diceRoll(10, 6, "e6kh6")
    print(f"rolls: {rolls}")
    print(f"info: {info}\n")

    rolls, info = diceRoll(1, 20, advantage="a")
    print(f"rolls: {rolls}")
    print(f"info: {info}\n")

    rolls, info = diceRoll(1, 20, advantage="d")
    print(f"rolls: {rolls}")
    print(f"info: {info}\n")