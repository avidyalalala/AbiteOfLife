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
def main_(n,x):
    print(x)
    print(n)
    if(n>=2):
        n=partion(n)
        temp_x=main_(n,x)
        temp_x=conquer(temp_x,x,n)
        return temp_x
    else:
        return temp_x

'''
failed end
'''
def _conquer(temp_x,n):
    if(i%2==0):
        temp_x=temp_x*temp_x
    return temp_x

i=2
def _main(x,n,boundry):
    global i
    temp_x=x
    print(i)
    print(temp_x)
    while(i<=boundry):
        temp_x=_conquer(temp_x,i)
        i=i*2 
        print(temp_x)
        print(i)
        _main(temp_x,i,boundry)
    if(i/2+1==n):
        temp_x=x*temp_x
        #print(i/2+1)
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
    n=11
    start=datetime.datetime.now()
    re=test(x,n)
    print("no_recur:"+str(re))
    end=datetime.datetime.now()
    print(end-start)
    print("right:"+str(main_(n,x)))
    #print(datetime.datetime.now()-end)
    print("^_^")
