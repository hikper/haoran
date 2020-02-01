import urllib.request,urllib.parse
import json,re

#Open isbn.txt to get isbn priviously stored
ISBN = open("isbn.txt",mode='r')
#Store those isbn in a list 
isbn = list()
#Open a file to store google books' id
output = open("id.txt",mode='w')
#A counter record the amount of books
count = 0
#dictionary
bookdict = dict()

for line in ISBN:
  isbn.append(line[:-1])
for bookisbn in isbn:
  try:
    
    #Make get request to google book api, using search by isbn
    data = urllib.request.urlopen("https://www.googleapis.com/books/v1/volumes?q="+bookisbn+"+isbn").read().decode()
    data = json.loads(data)
    #find the book's id
    id = data["items"][0]["id"]
    if id in bookdict:
      continue
    bookdict[id] = True
    output.write(id+"\n")
    count += 1
    print("Processing... ... ("+str(count)+"/"+str(len(isbn))+"): "+id)
  except:
    print("Processing... ... ("+str(count)+"/"+str(len(isbn))+"): "+bookisbn+" dones't match!")
print("Done! Next, run 'idToXlsx.py' !")

