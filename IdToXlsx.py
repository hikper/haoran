import requests,json,os,csv,xlsxwriter
import urllib.request
from bs4 import BeautifulSoup
from PIL import Image

#Open a folder to store photo, if it doesn's exist, create it
folder_path ='./photo/'
if (os.path.exists(folder_path) == False): 
    os.makedirs(folder_path)

#Set row 1 data name and format size
workbook = xlsxwriter.Workbook('bookList.xlsx')
worksheet = workbook.add_worksheet()
worksheet.set_column('A:A',30)
worksheet.write('A1', 'Cover')
worksheet.set_column('B:B',30)
worksheet.write('B1', 'Title')
worksheet.set_column('C:C',15)
worksheet.write('C1', 'Authors')
worksheet.set_column('D:D',15)
worksheet.write('D1', 'Publisher')
worksheet.set_column('E:E',15)
worksheet.write('E1', 'Categories')
worksheet.set_column('F:F',100)
worksheet.write('F1', 'Description')
worksheet.set_column('G:G',20)
worksheet.write('G1', 'PreviewLink')

#this is text format info 
wordFormat = {
    'font_size': 12,
    'align':'left',
    'valign':'vcenter',
    'font_name': u'微軟正黑體 Light',
    'text_wrap':True,
}
wordFormat = workbook.add_format(wordFormat)

#Open google book id list previous got
ID = open("id.txt").readlines()


row = 0
for id in ID:
    try:
        url = "https://www.googleapis.com/books/v1/volumes/"+id
        page = urllib.request.urlopen(url).read().decode()
        info = json.loads(page)
        row += 1
        try:
            id = info["id"]
        except:
            id = "null"
        try:
            title = info["volumeInfo"]['title']
        except:
            title = "null"
        try:
            authors = info["volumeInfo"]['authors']
        except:
            authours = list().append('null')
        try:
            publisher = info["volumeInfo"]['publisher']
        except:
            publisher = "null"
        try:
            description = info["volumeInfo"]['description']
        except:
            description = "null"
        try:
            categories = info["volumeInfo"]['categories']
        except:
            categories = "null"
        try:
            previewLink = info["volumeInfo"]['previewLink']
        except:
            previewLink = "null"

        #parse the html text
        description = BeautifulSoup(description,'html.parser')
        description = description.get_text()
        

        #write book data into excel 
        worksheet.set_row(row,200)
        worksheet.write(row, 1, title,wordFormat)
        worksheet.write(row, 2, authors[0],wordFormat)
        worksheet.write(row, 3, publisher,wordFormat)
        worksheet.write(row, 4, categories[0],wordFormat)
        worksheet.write(row, 5, description,wordFormat)
        worksheet.write(row, 6, previewLink,wordFormat)
        print("Processing... ...("+str(row)+'/'+str(len(ID))+') '+title)
        #add picture
        try:
            imageLink = ""
            for size in info["volumeInfo"]['imageLinks']:
                if size != 'extraLarge' and size != 'large':
                    imageLink = info["volumeInfo"]['imageLinks'][size]
            #donload picture
            photo = requests.get(imageLink)
            cover = open(folder_path+id+'.png','wb')
            cover.write(photo.content)
            cover.close()
            #adjust picture size
            adjpicture = folder_path+id+'.png'
            adjpicture = Image.open(adjpicture)
            (x,y) = adjpicture.size
            x_s = 250
            y_s = int(y * x_s / x)
            out = adjpicture.resize((x_s,y_s),Image.ANTIALIAS)
            out.save(folder_path+id+'.png')
            worksheet.insert_image(row, 0, folder_path+id+'.png', {'x_offset': 10, 'y_offset': 10,'x_scale': 0.65, 'y_scale': 0.65})
        except:
            worksheet.write(row, 0, "No picture", wordFormat)
    except:
        print("Processing... ...("+str(row)+'/'+str(len(ID))+') '+"Error! A book was dropped on the road!")
    
print("Done! All book's info were sent back form haoran lib! Open bookList.xlsx and enjoy ~★")
workbook.close()

