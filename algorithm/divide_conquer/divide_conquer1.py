
def divide(list):
    return 0

def conquer(i_p,list):
    pivot=list[i_p]
    for i in range(len(list)):
        if(list[i]>pivot and i<i_p):
            list[i_p]=list[i]
            list[i]=pivot
            i_p=i
        if(list[i]<pivot and i>i_p):
            list[i_p]=list[i]
            list[i]=pivot
            i_p=i

def quick_sort(list):
    i_p=divide(list)
    quick_sort(list)


if __name__=="__main__":
    list=[38,2,38,0,4,3,8,77,49,18,16,6,7,9,10]
    quick_sort(list)
