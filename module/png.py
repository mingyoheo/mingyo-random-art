#
# Mingyo Expression Generation
#
# Description: a module for combining matematical expressions randomly by recursive functions annd expressions
#
# Author: Mingyo Heo
# Date: oct 19, 2025
#
# input: getting recursive level and if it is unassigned, it is randomly used from 4 to 8.
# output: by using "buildExpr", it returns available matematical expressions
#



import random
from math import pi

# Recursive generate of math expression
# CurrentLevel: recusion level
def makeList(currentLevel, maxLevel):

    # If maximum level reached -> stop recusion
    if currentLevel >= maxLevel:
        randomConst = "{:.2f}".format(random.random() * 2 - 1)
        variables = ["x", "y", randomConst]
        return random.choice(variables)

    # 80% expand operator
    if random.randint(0, 9) < 8:
        operator = [" + "," - ", " * "]
        op = random.choice(operator)

        # Recursive generate two arguments
        arg1 = makeList(currentLevel + 1, maxLevel)

        arg2 = makeList(currentLevel + 1, maxLevel)
        return f"( {arg1} {op} {arg2} )"

    # 20% expand expression
    else:
        arg = makeList(currentLevel + 1, maxLevel)

        # Select one of four function forms
        mylist = [f"sin(2 * {arg})",
                  f"cos(1.5 * {arg})",
                  f"sin(3 * {arg})",
                  f"cos(5 * {arg})"]
        return random.choice(mylist)
    
# Function to initiate the expression generation process    
def buildExpr(level = None):
    if level is None:
        level = random.randint(4, 8)

    expr = makeList(0, level)
    return expr


def main():
    random.seed()

    print("make images")
    for i in range(5):
        print(f"{i}: {buildExpr()}\n")

# Only when png.py is run directly (not when imported)
if __name__ == "__main__":
    main()








































    
