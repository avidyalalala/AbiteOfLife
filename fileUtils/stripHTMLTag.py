import sys
import codecs
from BeautifulSoup import BeautifulSoup,Comment

#strip all the comments
def removeComments(soup):
    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    [comment.extract() for comment in comments]
    return soup

#strip all the style tag
def removeStyleTag(soup):
    styles=soup.findAll("style")
    for style_tag in styles:
        style_tag.extract()
    return soup

#strip all the script tag
def removeScriptTag(soup):
    scripts=soup.findAll("script")
    for script_tag in scripts:
        #script_tag.replaceWith("")
        script_tag.extract()
    return soup

def removeLinkNoContent(soup):
    onclicks=soup.findAll(onclick=True)
    notLinks=soup.findAll(href="#")
    for _a in onclicks+notLinks:
        _a.extract()
    return soup

def doWithBlank(soup):
    blanks=soup.findAll("&nbsp;");
    for blank in blanks:
        blank.replace_with(" ")    

    return soup 

def initContent(html):
    #in case the file includes multiple htmls
    soup=BeautifulSoup(html)
    soup=removeComments(soup)
    soup=removeStyleTag(soup)
    soup=removeScriptTag(soup)
    #soup=doWithBlank(soup)
    #content_body=soup.find("body")
    #if(content_body is not None):
    #    content = content_body
    #    text=text+''.join(content.findAll(text=True))
    content = soup
    text=''.join(content.findAll(text=True))
    return text 


def initRawData(input_path):
    rawdata=""
    try:
        rawdata=codecs.open(input_path,"r","gbk").read()
    except UnicodeDecodeError:
        try:
            rawdata=codecs.open(input_path,"r","utf-8").read()
        except:
            print("warning: %s cannot be decode"%input_path)
        #except UnicodeDecodeError:
        #    self.rawdata=open(self.input_path,"r").read()
            #print("cannot decode this file "+ self.input_path)
    except IOError:
        print("warning:this file is not exist "+ input_path)

    print(rawdata)
    return rawdata

if __name__=="__main__":
    if len(sys.argv)<2:
        print("Are You Kidding Me??? please input the source file path")
    else:
        source_path=sys.argv[1]
        html=initRawData(source_path)
        text=initContent(html)
        print(text)
