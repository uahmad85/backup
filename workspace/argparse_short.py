import argparse

parser = argparse.ArgumentParser(description='Short sample app')

parser.add_argument('-a', action="store", default=False)
parser.add_argument('-b', action="store", dest="b")
parser.add_argument('-c', action="store", dest="c", type=int)

args = parser.parse_args()
print args.c
print args.a
dic = { 'a': 1, 'b': 2 }
print dic[a]