from os import system


def controlledInput(MAX):
    while True:
        try:
            value = int(input('- '))
            if value > MAX:int('a') #on god
            break
        except:
            print('INVALID INPUT!\n')
    return value

def viewRolls():
    with open('files/rolls.txt','r',encoding='utf-8') as raw: rolls = [r.strip().split(':') for r in raw.readlines()]

    for r in rolls:
        per = 1-(float(r[-2])/float(r[-3]))
        if per > 0.4:
            print(r[-4],r[-3],r[-2])
        if float(r[-3])-float(r[-2]) > 400:
            print(r[-4],r[-3],r[-2])

    

def welcome():
    syslogo = r"""

    .----------------.  .----------------.  .----------------.  .----------------.  .----------------. 
    | .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
    | |  ____  ____  | || |              | || |  ___  ____   | || |     ____     | || | ____    ____ | |
    | | |_  _||_  _| | || |              | || | |_  ||_  _|  | || |   .'    `.   | || ||_   \  /   _|| |
    | |   \ \  / /   | || |    ______    | || |   | |_/ /    | || |  /  .--.  \  | || |  |   \/   |  | |
    | |    > `' <    | || |   |______|   | || |   |  __'.    | || |  | |    | |  | || |  | |\  /| |  | |
    | |  _/ /'`\ \_  | || |              | || |  _| |  \ \_  | || |  \  `--'  /  | || | _| |_\/_| |_ | |
    | | |____||____| | || |              | || | |____||____| | || |   `.____.'   | || ||_____||_____|| |
    | |              | || |              | || |              | || |              | || |              | |
    | '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
    '----------------'  '----------------'  '----------------'  '----------------'  '----------------' 
                                                                                                            
    """

    system("title " + 'X-Kom BOX')

    print(syslogo)
    print(f"1. Create new accs")
    print(f"2. Check old accs")
    
    pp = controlledInput(2)
    
    match pp:
        case 1:
            print("How many do you want to create? (MAX 50.)")
            amount = controlledInput(50)
            return 1,amount
        case 2:
            return 2,None
        #case 3:
        #    viewRolls()
        #    input("Press ENTER to close rolls...")