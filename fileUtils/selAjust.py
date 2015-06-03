import re

if __name__=="__main__":
    lines=open("/home/lina/sharedHOME/temp/sel.txt","r").readlines()
    _list=[]
    pattern=re.compile(r"^\|")
    for line in lines:
        words=line.split()
        _line=""
        for word in words[:4]:

            if(re.match(pattern,word)):
                print(word)
                _line=_line+"\t"+word
            else:
               # print(word)
                _line=_line+word+"|"
        _list.append(_line)
    _file=open("/home/lina/sharedHOME/temp/sel.txt.after","w")

    for line in _list:
        line=line.strip()
        _file.write(line+"\r\n")


