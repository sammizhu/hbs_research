import pandas as pd

with open('direct_match.csv', 'r') as t1, open('fuzzy_match.csv', 'r') as t2:
    fileone = t1.readlines()
    filetwo = t2.readlines()

with open('differences.csv', 'w') as outFile:
    for line in filetwo:
        if line not in fileone:
            outFile.write(line)
