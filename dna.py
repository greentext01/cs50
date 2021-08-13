import sys
import csv
import re


def str_repeat(str, dna):
    matches = re.findall(rf"(({str})+)", dna)

    if len(matches) == 0:
        return 0

    return len(max(matches)[0]) / len(str)


def main():
    if(len(sys.argv) != 3):
        print("Usage: python dna.py data.csv sequence.txt")
        return

    data = open(sys.argv[1])
    reader = csv.DictReader(data)
    dna = open(sys.argv[2]).read()

    for line in reader:
        name = ""
        matches = 0

        for row in line:
            if row == "name":
                name = line[row]
                continue

            if str_repeat(row, dna) == int(line[row]):
                matches += 1

        if matches == len(line) - 1:
            print(name)
            return

    print("No match")


if __name__ == "__main__":
    main()
