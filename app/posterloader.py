#you might want to set up a virtual environment in order to do this
from PIL import Image, ImageFont, ImageDraw
#module to read in CSV files
import csv
#not important. just for making the test CSV file
import pandas
#this will be helpful when doing the math to figure out how many rows that you need in this image
import math

FOLDFERNAME = "uploads"

#decided to go ahead and make lists for each year. easy to switch up the names here if the CSV has different ways of listing the years
years = {
    "faculty":[],
    "first":[],
    "second":[],
    "third":[],
    "fourth":[]
}
#maximum size of our images inside the canvas
size = 256, 256

#the size of our canvas t
canvasSize = 300

#the font that we use. not super important. also the size of the font
font = ImageFont.truetype("arial.ttf", 20)
font2 = ImageFont.truetype("arial.ttf", 30)

def rowsNumber(yearList):
    return math.ceil(len(yearList)/20)

def totalHeight():
    totalRows = 0
    for yearList in years.values():
        #this lets us separate rows by year instead of having all years grouped together
        totalRows += rowsNumber(yearList)    
    return totalRows*350 + 250   #added extra space for formatting

#to get the individual height of rows for each category
def rowsHeight(yearList):
    rowsHeight = rowsNumber(yearList)
    return rowsHeight*350 - 50

def readCSV():
    #can replace with the actual CSV name. this opens up the CSV file and then reads in the data so that we can make the list of image object
    with open('images.csv', newline='') as info:
        #this lets us iterate over the rows of the CSV files
        reader = csv.DictReader(info)
        #this iterates over the rows of the CSV file
        for row in reader:
            #each year is like the year in college. it will have the image for each person in that year
            if row["year"] != "year":
                #the canvas on which we draw the picture of the person and the text
                canvas = Image.new("RGB", (canvasSize, canvasSize), (255, 255, 255))
                # get a drawing context (a way to draw onto the canvas)
                d = ImageDraw.Draw(canvas)
                #put the pic on the canvas
                #load the picture from the filename in the CSV file
                picture = Image.open(FOLDFERNAME + "/" + row["filename"])
                #make the picture have a max of 256 in either dimension (resize it)
                picture.thumbnail(size)
                #get the actual size of the picture
                width, height = picture.size
                #where do we put the picture on our canvas? a little bit of math to make sure we center it
                offsetImg = (150-width//2, 10)
                #draw the picture onto the canvas
                canvas.paste(picture, offsetImg)

                #put the text on the canvas. get the size so that we can center it
                text_width, text_height = font.getsize(row["name"])
                #make the position so that the text is centered and starts 30 pixels over the bottom
                offsetTxt = (150-text_width//2, 270)
                #draw the text onto the canvas
                d.text(offsetTxt, row["name"].title(), fill=(0, 0, 0), font=font)

                #add the picture to our dictionary of years
                years[row["year"]].append(canvas)

                #comment these out when not testing
                canvas.save("new duck.jpg","JPEG")

def sizePoster():
    pass

def testCSV():
     #this creates a csv on which we can test the code. not super important
     df =  pandas.DataFrame({'name':["duck"],'year':['third'], 'filename':['duck.jpg']})
     df.to_csv('images.csv',index=False)
    
def test():
    #this is even less important than testCSV
    print("test code.")
    
def canvas():
    readCSV()
    # the global canvas on which we draw the pictures and text
    canvas = Image.new("RGBA", (7200, totalHeight()), (255, 255, 255,1))
    # local canvas for drawing texts
    canvas2 = Image.new("RGB", (4000, 150), (221, 237, 235))
    # get a drawing context
    d = ImageDraw.Draw(canvas2)
    #put the text on the canvas. get the size so that we can center it
    text_width, text_height = font.getsize("Smith College Computer Science Department")
    #make the position so that the text is centered 
    offsetTxt = (2000-text_width//2, 40)
    #draw the text onto the local canvas
    d.text(offsetTxt, "Smith College Computer Science Department", fill=(0, 0, 0), font=ImageFont.truetype("arial.ttf", 50))
    # draw text with local canvas unto the global canvas
    canvas.paste(canvas2, (1600, 50))
    
    headers = []
    # create list of keys to enable indexing
    for level in years.keys():
        headers.append(level)
    
    # declare variables for dimensions and set default values
    indx, x, y, z = 0, 180, 250, 250
    #iterate over values stored in lists
    for picture_list in years.values():
        #account for empty lists to avoid building excess negative space
        if len(picture_list) != 0:
            # create labels for each category on a local canvas and draw to global canvas
            canvas2 = Image.new("RGB", (rowsHeight(picture_list), 80), (221, 237, 235))
            d = ImageDraw.Draw(canvas2)
            text_width, text_height = font.getsize(headers[indx])
            offsetTxt = (rowsHeight(picture_list)/2-text_width//2, 30)
            d.text(offsetTxt, headers[indx].title(), fill=(0, 0, 0), font=font2)
            canvas2 = canvas2.rotate(90, expand=1)
            canvas.paste(canvas2, (50, z))
            
            # iterate over pictures in each category and draw to global canvas
            for picture in picture_list:
                canvas.paste(picture, (x, y))
                x += 350
                #account for boundaries
                if x >= 6850:
                    x = 180
                    y += 350
            #this begins a fresh row for each new category.
            y += 350
            x = 180
            z += rowsHeight(picture_list) + 50
        #increment list index
        indx += 1
   #show all the pictures
    canvas.save("text2.png","PNG")
    canvas.show()

if __name__ == "__main__":
    #run code
    canvas()
