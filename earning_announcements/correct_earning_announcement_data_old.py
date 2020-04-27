import os
import fileinput


directory = "../samples/earning announcement data/"

for filename in os.listdir(directory):
    start = True
    for line in fileinput.input(directory+filename, inplace=True):
        if start:
            start = False
            print(line, end="")
            continue
        splits = line.split(',')
        del splits[-3]
        final_line = ','.join(splits)
        print(line.replace(line, final_line), end="")
