def test_main():
    print('this is main func')

def main():
    test_main()

main()

if __name__ == '__main__':
    print 'mainfunc file is being execute'
else:
    print 'mainfunc being imported'
    