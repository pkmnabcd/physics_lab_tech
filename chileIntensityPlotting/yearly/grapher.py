from sys import argv
if __name__ == "__main__":
    if len(argv) == 1:
        print("USAGE: python[3] grapher.py path_to/[year]dailyAverages.csv")
        exit()
    averagesPath = argv[1]
