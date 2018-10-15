from PIL import Image
from colorNames import ColorNames
import os, sys
import pyautogui

#import pdb;

startOfCanvasX = 490
startOfCanvasY = 255
downscaleFactor = 5

testArr2D = [['1','2','3','4'],['5','6','7','8'],['9','10','11','12'],['13','14','15','16'],['17','18','19','20']]
testArr = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20']
def aspectRatio(image):
    w, h = image.size
    aspRatio = w/h
    neededAspRatio = 815/610 #size of canvas
    if aspRatio < neededAspRatio:
        return 'narrow'
    elif aspRatio > neededAspRatio:
        return 'wide'
    elif aspRatio == neededAspRatio:
        return 'good'

def resizeImage(type,w,h,image):
    if type == 'narrow':
        w , h = image.size
        ratio = 610 / h
    elif type == 'downscale':
        ratio = 1/downscaleFactor  # 1/3
    else: #else includes 'wide' and 'good', both of which this the w ratio works for
        w , h = image.size
        ratio = 815 / w
    size = int(w * ratio), int(h * ratio)
    return image.resize(size)

def whiteBars(image,newW,newH):
    old_size = image.size
    new_size = (newW, newH)
    new_im = Image.new("RGB", new_size, "white")
    new_im.paste(image, (int((new_size[0]-old_size[0])/2),int((new_size[1]-old_size[1])/2)))
    return new_im

def createColorArr(width,height):
    arr = []
    for y in range(height):
        for x in range(width):
            r,g,b = image.getpixel((x,y))
            colorName = (ColorNames.findNearestImageMagickColorName((r,g,b)))
            arr.append(colorName)
    return arr

def selectColor(color):
    color = int(color) - 1
    y = startOfCanvasY + 625
    if color - 11 >= 0: #F:2,9  --- T:11,22
        color += -11
        y += 25
    x = 595 + (color * 23)
    pyautogui.moveTo(x,y)
    pyautogui.click()

def draw(arr,width,height):
    pyautogui.PAUSE = 1
    pyautogui.FAILSAFE = True

    lastCol = "yeet"
    for j in range(0,height): #203- height
        for i in range(0,width): #271- width
            x = (i*downscaleFactor)+startOfCanvasX
            y = (j*downscaleFactor)+startOfCanvasY
            arrPos = i + (width * (j))
            thisCol = arr[arrPos]
            if thisCol != lastCol:
                selectColor(thisCol)
                lastCol = thisCol
            if thisCol != "1":
                pyautogui.moveTo(x,y)
                pyautogui.click()

def my_max_by_weight(sequence):
    if not sequence:
        raise ValueError('empty sequence')

    maximum = sequence[0]

    for item in sequence:
        # Compare elements by their weight stored
        # in their second element.
        if item[1] > maximum[1]:
            maximum = item

    return maximum

def arrLineConversion(arr, width, height):
    twoDArr = [] #arr, but formatted as a 2D array. [Y][X].
    lineArr = []

    for j in range(0,height):
        twoDArr.append([])
        for i in range(0,width):
            twoDArr[j].append(arr[i + (width * (j))]) #Array with x,y coords of pixel data. Starts w/ 0,0.
    #pdb.set_trace()

    for l in range(0,height): #Loops through each pixel in each row of picture.
        a = 0 #Sets a to 0 for while loop.
        while a < width - 1: #Loops through each pixel in each column of picture.
            if (twoDArr[l][a+1] != twoDArr[l][a]) or  (a == width - 1): #Can assume that pixel is an ending point if true. Compares next color to current pixel color.
                highestDot = -1 #Defaults the highest dot number (dot meaning end point x value) to negative one, which cannot exist.
                if len(lineArr) != 0: #If the array is empty, then there are not any end points yet.
                    for z in range(len(lineArr)-1,0,-1): #Counts down from size of lineArr to 0.
                        if lineArr[z][1] == l: #Searching for the highest 'x' value of the ending points of the same 'y' value.
                            print('pass  ', z, a, l, lineArr[z][1], lineArr[z][0], len(lineArr))

                            highestDot = lineArr[z][0] #The highest dot in each row that gets compared to a given dot, dictating the length if this exists.

                            break #Breaks once the highest 'x' value of the ending points of the same 'y' value is found.
                        else:
                            print('FAIL  ', z, a, l, lineArr[z][1], lineArr[z][0], len(lineArr))
                if highestDot == -1: #If highestDot is still -1, then that means that there is not a end point before the given end point on the same row.
                    dotDif = width - (width - a) #Sets the amount of pixels needed to be drawn behind the end point to given point to the first pixel in the same row.
                elif highestDot > -1: #If highestDot is not negative, it means that there is another end point before the given endpoint on the same row.
                    dotDif = abs(a - highestDot) #The dotDif is one less than the difference of a and highestDot when there is another end point before the given endpoint on the same row.
                lineArr.append([a,l,dotDif,twoDArr[l][a]]) #Appends an array to lineArr that contains [x coord of end point, y coordof end point, how many more pixels need to be drawn before than endpoint of the same color, the color of the endpoint].
                #print(dotDif, highestDot)

            a+=1 #Increments while loop
    return lineArr #Returns lineArr to called function

def drawRev2(arr,width,height):
    pyautogui.PAUSE = .0000000001
    pyautogui.FAILSAFE = True

    for j in range(0,len(arr)-1):
        x = (arr[j][0]*downscaleFactor)+startOfCanvasX
        y = (arr[j][1]*downscaleFactor)+startOfCanvasY
        sub = (x+arr[j][2]*downscaleFactor)
        thisCol = arr[j][3]
        selectColor(thisCol)
        if thisCol != "1":
            pyautogui.moveTo(x,y)
            pyautogui.mouseDown()
            pyautogui.moveTo(x-sub,y)
            pyautogui.mouseUp()



path = r'picture' + '\\' + os.listdir(r'picture')[0]
image = Image.open(path)
type = aspectRatio(image)
image = resizeImage(type,'null','null',image)
image = whiteBars(image,815,610)
image = resizeImage('downscale',815,610,image)
#image.save(path, "PNG")
newSizeX = int(815 * (1/downscaleFactor))
newSizeY = int(610 * (1/downscaleFactor))
origArr = createColorArr(newSizeX,newSizeY)

#print(arrLineConversion(origArr,newSizeX,newSizeY))
#newArr=arrLineConversion(origArr,newSizeX,newSizeY) #Real
newArr=arrLineConversion(testArr,4,5) #Test
#drawRev2(newArr, newSizeX, newSizeY)

#colors = createColorArr(newSizeX,newSizeY)
#draw(colors,newSizeX,newSizeY)


#for i in range(1,23):
#    selectColor(i)

#   board:
#   490,225 -> 1305, 835

#   X values: (x,855)     (x, 880)
#   595, 619, 643, 667, 691, 715, 739, 763, 787, 807, 835
