import sys

def isPrimeNumber(_num):
    for value in range(1,_num-1):
        if(_num%value!=0):
            return False

    return True
    


if __name__=="__main__":
    input=sys.argv[1]
    text=""
    re=isPrimeNumber(int(input))
    if(re is not True):
        text=" not"

    print("the number you input %s is%s a Prime Number."%(input, text))
    
	
