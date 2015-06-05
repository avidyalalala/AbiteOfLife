import re
def method1():
    pro1=0
    def method2():
        pro2=1
        print(pro1)
        return
    method2()
    return pro1
    #return pro2

if __name__=="__main__":
    print(method1())

    lines=open("/home/lina/sharedHOME/temp/sel.txt","r").readlines()
    _list=[]
    pattern=re.compile(r"^\|")
    for line in lines:
        words=line.split()
        _line=""
        for word in words:

            if(re.match(pattern,word)):
                _line=_line+"\t"+word
            else:
               # print(word)
                _line=_line+word+"|"
        _list.append(_line)
    _file=open("/home/lina/sharedHOME/temp/sel.txt.after","w")

    for line in _list:
        line=line.strip()
        _file.write(line+"\r\n")


