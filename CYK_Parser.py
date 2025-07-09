# 801420902
# ITCS 6114 - Project 2

import sys
from collections import defaultdict


# Task1: Reading the grammar
def readGrammar(grammarIN):
    # Processing the grammar into efficient lookup tables for terminals and pairs of non-terminals.

    # Using defaultdict so that there is no duplicates of a rule
    terminalRules = defaultdict(set)  # used to store terminal rules in dictionary
    pairRules = defaultdict(set)  # used to store non terminal pair rules in dictionary

    for line in grammarIN.strip().split("\n"):
        lhs, rhs = line.split("->")  # Splitting the line into lhs and rhs
        lhs = lhs.strip()
        productions = [prod.strip() for prod in rhs.split("|")]  # Splitting rhs into productions
        for prod in productions:
            if len(prod.split()) == 1:  # If the production is a single terminal
                terminalRules[prod].add(lhs)  # we add lhs to the set of terminal rules for this production
            else:
                pairRules[tuple(prod.split())].add(lhs)  # if its pair of terminals we add lhs to the set of pair rules for this production

    return terminalRules, pairRules


def cykParse(terminalRules, pairRules, string):
    n = len(string)
    table = [[set() for _ in range(n)] for _ in range(n)]  # constructing a table of size nxn

    # Storing terminal rules
    for i in range(n):  # for each element in string
        if string[i] in terminalRules:  # If the element is a terminal then we store it in diagonal
            table[i][i] = terminalRules[string[i]]

    # filling the table that represents which non-terminals can generate each possible substring of the input string.
    for L in range(2, n + 1):
        for i in range(n - L + 1):  # Iterate over starting indices for the substring
            j = i + L - 1  # Calculating the end index for the substring
            for k in range(i, j):
                leftCell = table[i][k]  # Getting the set of non-terminals for the left substring
                rightCell = table[k + 1][j]  # Getting the set of non-terminals for the right substring
                for b in leftCell:  # updating the cell with rules lhs if the pair b,c is a valid rule
                    for c in rightCell:
                        if (b, c) in pairRules:
                            table[i][j].update(pairRules[(b, c)])

    # Check if start symbol is in the top-right cell
    startSign = "S" if any("S" in values for values in pairRules.values()) else "Sent"
    accepted = 1 if startSign in table[0][n - 1] else 0  # Checking if the start symbol is in the top-right cell

    return accepted, tableChange(table)  # returning that the string is acceptable or not and changing table acc to output


def tableChange(table):  
    """
    Formatting the table so it is according to project output requirements.
    Ensures the lower triangular portion remains empty.
    """
    newTable = []
    n = len(table)
    for i in range(n):
        newRow = []
        for j in range(n):
            if j < i:
                # Leave the lower half of the table empty
                newRow.append("")
            elif table[i][j]:
                # Join sorted non-terminals with ", " for proper formatting
                newRow.append(", ".join(sorted(table[i][j])))
            else:
                # Add "-" for empty cells in the upper triangular part
                newRow.append("-")
        # Join cells in a row with "; " for proper formatting
        newRowInput = "; ".join(newRow)
        newTable.append(newRowInput)
    # Join rows with newline characters
    return "\n".join(newTable)



def main():
    if len(sys.argv) != 4:
        print("Usage: python project.py <grammar file> <input string file> <output file>")
        sys.exit(1)

    grammarFile = sys.argv[1]  # input grammar file
    stringFile = sys.argv[2]  # input string file
    outputFile = sys.argv[3]  # output file with name of the stringfile

    # Reading grammar file and processing it
    with open(grammarFile, "r") as file:
        grammarIN = file.read()
    terminalRules, pairRules = readGrammar(grammarIN)

    # Task2:
    # Reading input string from file and splitting and stripping off white spaces
    with open(stringFile, "r") as file:
        inputString = file.read().strip().split()

    # running cyk
    accepted, table = cykParse(terminalRules, pairRules, inputString)

    # Write output to file
    with open(outputFile, "w") as file:
        file.write(f"{accepted}\n")  # if string is accepted or not
        file.write(table)

    print(f"The output is written to {outputFile}")


if __name__ == "__main__":
    main()
