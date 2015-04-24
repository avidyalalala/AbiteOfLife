def divide(arr):
    length=len(arr)
    if(length%2==0):
        return length/2
    else:
        return (length-1)/2

def conquer(i_p, arr):
    list_less=[]
    list_more=[]
    list_equal=[]
    for i in range(len(arr)):
        pivot=arr[i_p]
        if(arr[i]>pivot):
            list_more.append(arr[i])
        elif(arr[i]<pivot):
            list_less.append(arr[i])
        else:
            list_equal.append(arr[i])
    return list_less,list_more,list_equal
 
def quick_sort(arr):
    if(len(arr)<=1):
        return arr

    i_p=divide(arr)
    list_less,list_more,list_equal=conquer(i_p,arr)
    re_less=quick_sort(list_less)
    re_more=quick_sort(list_more)
    return re_less+list_equal+re_more
    

if __name__=="__main__":
    arr=[11,4,6,10,5,29,2,9,4,38,100,4,5,2,1,7,8]
    re=quick_sort(arr)
    print(re)
