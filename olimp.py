ints = list(map(int,input().split('-')))

def main(ints):
    for chislo in ints:
        while chislo %5 != 0 or chislo%7 != 0:
            if chislo == 1:
                return 'No'
            chislo -= 3
            if chislo < 0:
                return 'No'
    return 'Yes'

if __name__ == '__main__':
    print(main(ints))