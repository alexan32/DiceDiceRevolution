# DiceDiceRevolution
A simple system for parsing dicestrings

Takes strings in dice notation as input, and evaluates the expression before returning the result. Additionally allows for variables to be in the expression and provides additional options to further modify how the dice are rolled.

If you want to dive into the code, start with main.py(./src/main.py)

Usage example:

```python
dp = DiceProcessor()
total, info = dp.processDiceString("6d6 + 3(1d6 - 2)")
```

the processDiceString function returns a tuple containing the total as an integer, as well as an expression which demonstrates more details about the results of the roll.

there is an optional argument called "advantage", which can be set with a value of either "a" or "d", and is used as shorthand to modify dice expressions that use "1d20"

```python
total, info = dp.processDiceString("1d20 + prof + dex", {"prof": "2", "dex": "3"}, advantage="a")
```