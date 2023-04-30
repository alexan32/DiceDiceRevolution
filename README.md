# DiceDiceRevolution
## A simple system for parsing dicestrings

Takes strings in dice notation as input, and evaluates the expression before returning the result. Additionally allows for variables to be in the expression and provides additional options to further modify how the dice are rolled.

If you want to dive into the code, start with [main.py](./src/main.py)

## Usage example:

```python
dp = DiceProcessor()
total, info = dp.processDiceString("6d6 + 3(1d6 - 2)")
print(info)
```

Ouput: 
```
  6d6['4', '!6', '4', '2', '5', '4'](25) + 3 * 1d6['4'](4) - 2 = 31
```

The processDiceString function returns a tuple containing the total as an integer, as well as an expression which demonstrates more details about the results of the roll.

There is an optional argument called "advantage", which can be set with a value of either "a" or "d", and is used as shorthand to modify dice expressions that use "1d20"

```python
  total, info = dp.processDiceString("1d20 + prof + dex", {"prof": "2", "dex": "3"}, advantage="a")
```

## Dice Modifiers

You can add modifiers to the dice notation to modify a dice roll. Use the following modifiers and selector to alter the the way dice are rolled.
### Modifiers
- 'k' keep selection
- 'p' drop selection
- 'rr' reroll on when landing on X
- 'ro' reroll once
- 'e' explode when landing on X
- 'mi' set minimum value a roll can land on
- 'ma' set maximum value a roll can land on

### Selectors
- 'X' whole number representing a face value on the di
- 'hX' highest X results
- 'lX' lowest X results
- '<X' less than X
- '>X' greater than X

example:
```
  dp = DiceProcessor()
  print(dp.processDiceString("4d6kh3")[1])
```
output:
```
  4d6kh3['~1', '4', '4', '5'](13) = 13
```

