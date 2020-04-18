#author: Arib Dhuka
#import image library
from PIL import Image
import sys
import re

DEFAULT_PERCENT = 10

def imageborderpx(img, pxamt, clr):
    #get size
    width, height = img.size
    
    #create new image with proper size
    newimg = Image.new(mode="RGBA", size = (width+(pxamt*2), height+(pxamt*2)), color = clr)

    #paste image 
    newimg.paste(img, (pxamt,pxamt))

    return newimg


def imageborderpercent(img, percent, clr):
    percent = percent / 100
    #get size
    width, height = img.size
    #add percentage to each size
    pxamt = width*percent
    pxamt += height*percent
    pxamt /= 2
    pxamt = int(pxamt)
    #add border as pixel
    return imageborderpx(img, pxamt, clr)
    

def imageconvert(imgPath, options):
    #see if we can open the image
    try:
        img = Image.open(imgPath)
    except IOError:
        print("Image not found for:", imgPath)
        return
    amount, method = options['size']
    #check sizing method to know where to send it
    if method == "%":
        newimg = imageborderpercent(img, amount, options['color'])
    else:
        newimg = imageborderpx(img, amount, options['color'])

    #get file name and extension
    lastdotindex = imgPath.rindex(".")
    extension = imgPath[lastdotindex:]
    #check for extension change
    if options['ext'] != "undef":
        extension = options['ext']
    #create new filename
    newFilename = imgPath[0:lastdotindex] + "-border" + extension

    #remove alpha channel for jpegs
    if extension == ".jpeg" or extension == ".jpg":
        newimg = newimg.convert('RGB')
    #attempt to save
    try:
        newimg.save(newFilename)
        print(newFilename, "complete!")
    except IOError:
        print("So close! We had trouble saving the file.")
    


#Help dialog
def displayHelp():
    print("Help - AddBorder")
    print("Usage: addborder [filepaths(s)] (Options)")
    print("\tOptions:")
    print("\t\t--help")
    print("\t\t\tDisplays this dialog")
    print("\t\t--color=[R,G,B|R,G,B,A]")
    print("\t\t\tChoose the color for the border")
    print("\t\t--size=[Xpx | X%]")
    print("\t\t\tChoose the border size as a pixel amount or pecent")
    print("\t\t--ext=[.jpeg|.png|.gif]")
    print("\t\t\tChoose a file extension if you want it to be different than the original")
    print("\tExample: addborder image.png --color=255,255,255 --size=10%")

#color input validation
def getColor(arg):
    argsplit = arg.split(',')
    #check to ensure correct format
    if len(argsplit) < 3:
        print("Not enough values for a color!")
        return (255,255,255,0)
    if len(argsplit) > 3:
        print("Too many values for a color!")
        return (255,255,255,0)
    #convert each item to int
    for i in range(0, len(argsplit)):
        try:
            argsplit[i] = int(argsplit[i])
        except ValueError:
            print("Couldn't parse your color... defaulting to white")
            return (255,255,255,0)
    #if only 3 arguments add a 0
    if len(argsplit) == 3:
        argsplit.append(255)
    #convert to tuple
    return tuple(argsplit)

#size input validation
def getSize(arg):
    #input must match regex
    regex = re.compile("[0-9]+px")
    regex2 = re.compile("[0-9]+%")
    regex3 = re.compile("[0-9]")
    if regex.match(arg) and regex2.match(arg) and regex3.match(arg):
        print("Size doesn't match format check help guide.")
        return (DEFAULT_PERCENT, "%")
    #parse px
    if arg[-2:] == "px":
        try:
            amt = int(arg[0:-2])
            return (amt, "px")
        except ValueError:
            print("Couldn't parse your size... defaulting to ", DEFAULT_PERCENT, "%", sep="")
            return (DEFAULT_PERCENT, "%")
    #parse percentage
    elif arg[-1] == "%":
        try:
            amt = int(arg[0:-1])
            return (amt, "%")
        except ValueError:
            print("Couldn't parse your size... defaulting to ", DEFAULT_PERCENT, "%", sep="")
            return (DEFAULT_PERCENT, "%")
    #if no units assume %
    else:
        print("No units declared for size... assuming %")
        try:
            amt = arg
            return (amt, "%")
        except ValueError:
            print("Couldn't parse your size... defaulting to ", DEFAULT_PERCENT, "%", sep="")
            return (DEFAULT_PERCENT, "%")


def main():
    #check argument size
    arglen = len(sys.argv)
    #if not enough arguments display help... because they must need it
    if(arglen == 1):
        displayHelp()

    #remove filename from arg list
    sys.argv.remove(sys.argv[0])
    
    #default options
    options = {}
    options['color'] = (255,255,255)
    options['size'] = (DEFAULT_PERCENT,"%")
    options['ext'] = "undef"

    fileQueue = []
    #for each argument
    for arg in sys.argv:
        #if its color
        if arg[0:8] == "--color=":
            options['color'] = getColor(arg[8:])
        #if its size
        elif arg[0:7] == "--size=":
            options['size'] = getSize(arg[7:])
        elif arg[0:6] == "--ext=":
            options['ext'] = arg[6:]
        elif arg[0:6] == "--help":
            displayHelp()
        #else add the file to the list of borders to add
        else:
            fileQueue.append(arg)

    #handle each file
    for img in fileQueue:
        imageconvert(img, options)

if __name__ == "__main__": 
    main()