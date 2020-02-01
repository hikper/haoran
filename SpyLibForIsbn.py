import urllib.request, urllib.parse, urllib.error,re
from bs4 import BeautifulSoup

#Open the library new book page
#Because the page has oauth authenization system, I can't automate this part temporarily
ourl = input('input url:')
try:
    total = int(input('Roughly, how many books you want?:'))
except:
    print("Please enter integer")
    exit()

ourl = re.findall("(.*)func=", ourl)[0]+"func=short-jump&jump="
page = 1
count = 0
#Store the result isbn in myfile,isbn.txt
myfile = open('isbn.txt',mode='w',encoding='utf8')

#A dictionary to check if some book repeatly crawl
dictionary = dict()

while count <= total :
    #Rewrite url to flip page
    url = ourl+str(page)
    try:
        library = urllib.request.urlopen(url).read().decode()
    except:
        print('url:'+url+' is invalid!')
        break
    page += 20
    #Extract isbn on page by regular expression
    ISBN = re.findall("var update_isbn='([-0-9]*)';",library)
    for isbn in ISBN:
        if isbn in dictionary:
            continue
        else:
            dictionary[isbn] = True
        isbn = re.sub('-','',isbn)
        myfile.write(isbn)
        myfile.write('\n')
        count += 1 
        print("Processing... ...("+str(count)+"/"+str(total)+"): ",isbn)
        if count >= total:
            break
print("Done! The crawler spy has bring enough isbn from haoran website. Next, run 'UseIsbnForId.py'. ")



