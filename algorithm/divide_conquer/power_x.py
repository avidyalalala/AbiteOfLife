import datetime
'''
failed start
'''
def partion(n):
    if(n%2==0):
        n=n/2
    else:
        n=(n-1)/2
    #print(n)
    return n

def conquer(temp_x,x,n):
    if(n%2==0):
        temp_x=temp_x*temp_x
    else:
        temp_x=temp_x*temp_x*x
    return temp_x

'''
x is like coefficient or constant,
in the whole procedure, x is never be modified
'''
def power(n,x):
    #print(n)
    #print(x)
    if(n==0):
        return 1
    else:
        old_n=n
        n=partion(n)
        temp_x=power(n,x)
        temp_x=conquer(temp_x,x,old_n)
        #print(temp_x)
        #print("")
        return temp_x

def test(x,n):
    i=2
    temp=x
    while(i<=n):
        temp=temp*x
        i+=1
    return temp

if __name__=="__main__":
    x=2
    n=200
    start=datetime.datetime.now()
    re=test(x,n)
    print("no_recur:"+str(re))
    end=datetime.datetime.now()
    print(end-start)
    print("right:"+str(power(n,x)))
    print(datetime.datetime.now()-end)
    print("^_^")
