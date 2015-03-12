import sys, csv
from operator import itemgetter

namedict = {}

def add_names(namedict, names):
    for name in names:
        if name in namedict:
            namedict[name] += 1
        else:
            namedict[name] = 1

def pull_names(line):
    return [ line[i] for i in filter(lambda x: x%2==0, range(4,17)) ]

def main():
    filename = '2015leaderboard.tsv'

    if len(sys.argv) == 2:
        filename = sys.argv[1]
    try:
        with open(filename) as infile:
            leader = csv.reader(infile, delimiter='     ')
            next(leader)
            for line in leader:
                add_names(namedict, pull_names(line))
            for baz in sorted(namedict.iteritems(), key=lambda item: item[1], reverse=True):
                print '{0}: {1}'.format(baz[0], baz[1])

    except:
        print sys.exc_info()



if __name__ == '__main__':
    main()


