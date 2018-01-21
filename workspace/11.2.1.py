import re

def getAverage(filename):
    f = open(filename, 'r')
    matches = []
    for line in f:
        matches.extend(re.findall('^New Revision: (\d+)', line))
    fltmatches = [float(x) for x in matches] #convert values to floats
    average = sum(fltmatches) / len(fltmatches)
    return average

def main():
    """Main program loop"""
    filename = raw_input("Enter file: ")
    average = getAverage(filename)
    print average

if __name__ == '__main__':
    main()
