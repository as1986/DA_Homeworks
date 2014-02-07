#!/usr/bin/python


def main():
    import sys
    with open(sys.argv[1]) as f:
        import csv
        iReader = csv.reader(f)
        rows = [r for r in iReader][1:]
        colsToWrite = [(r[0], r[1], r[2], r[6]) for r in rows]
        with open(sys.argv[2], 'w') as wFile:
            for row in colsToWrite:
                wFile.write(' '.join(row) + '\n')
    return

if __name__ == '__main__':
    main()
