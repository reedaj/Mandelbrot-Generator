#Written by Adam Reed
import numpy
import time
from numba import jit
from PIL import Image
import multiprocessing as mp

#size of the image
resolutionMultiplier = 1
width = 1920 * resolutionMultiplier
height = 1080 * resolutionMultiplier

#Zoom Control. Possible usable when zooming closer into the image

zoom = 5

#Offset to center the image
center = -1.3933618941977570226953275778214447200298309326171875 + 0.00415573916836028782462175712453245068900287151336669921875j
#Increase iterations to impove the quality of the image
iterations = 500



@jit
def mandelbrot( c, n, iterations ):
    currentOutput = c
    for i in range(0, iterations):
        currentOutput = currentOutput**n + c
        if abs(currentOutput) > 2:
            return i

    return currentOutput



#Progress bar to get an idea of when the image will be
def progressIndication(x, screenSize):
    if x%32==0:
        prog = x/screenSize*100
        print(str(prog) + "% done", end="\r")

#Generate the array for a single image

def generator(widthStart, widthEnd, width, height, iterations, zoom, center, n, return_value):
    data = numpy.zeros((height, widthEnd-widthStart, 3), dtype=numpy.uint8)
    for x in range(0, height-1):
        for y in range(0,  widthEnd-widthStart):
            c = zoom*((y+widthStart)/width - 0.5 + ((x/height)-0.5)*1j)
            c = c + center

            #Check how fast the point is shooting off to infnity
            delta = abs(mandelbrot( c, n, iterations ))*2
            #print (delta)
            data[x, y] = [delta*4, delta, delta/4]

        #progressIndication(x, height)
    return_value[0] = data

def createFrame(n, i):
    #Split the process into 8 pieces.
    manager = mp.Manager()
    imageData0 = manager.dict()
    imageProcess0 = mp.Process(target=generator, args=(0,int(round(width/8)),width,height,iterations,zoom,center,n,imageData0))

    imageData1 = manager.dict()
    imageProcess1 = mp.Process(target=generator, args=(int(width/8),int(2*width/8), width, height,iterations,zoom,center,n,imageData1))

    imageData2 = manager.dict()
    imageProcess2 = mp.Process(target=generator, args=(int(2*width/8),int(3*width/8), width, height,iterations,zoom,center,n,imageData2))

    imageData3 = manager.dict()
    imageProcess3 = mp.Process(target=generator, args=(int(3*width/8),int(4*width/8), width, height,iterations,zoom,center,n,imageData3))

    imageData4 = manager.dict()
    imageProcess4 = mp.Process(target=generator, args=(int(4*width/8),int(5*width/8), width, height,iterations,zoom,center,n,imageData4))

    imageData5 = manager.dict()
    imageProcess5 = mp.Process(target=generator, args=(int(5*width/8),int(6*width/8), width, height,iterations,zoom,center,n,imageData5))

    imageData6 = manager.dict()
    imageProcess6 = mp.Process(target=generator, args=(int(6*width/8),int(7*width/8), width, height,iterations,zoom,center,n,imageData6))

    imageData7 = manager.dict()
    imageProcess7 = mp.Process(target=generator, args=(int(7*width/8),int(8*width/8), width, height,iterations,zoom,center,n,imageData7))

    imageProcess0.start()
    imageProcess1.start()
    imageProcess2.start()
    imageProcess3.start()
    imageProcess4.start()
    imageProcess5.start()
    imageProcess6.start()
    imageProcess7.start()

    imageProcess0.join()
    imageProcess1.join()
    imageProcess2.join()
    imageProcess3.join()
    imageProcess4.join()
    imageProcess5.join()
    imageProcess6.join()
    imageProcess7.join()

    totalImage = imageData0.values()[0]
    totalImage = numpy.append(totalImage, imageData1.values()[0], axis=1)
    totalImage = numpy.append(totalImage, imageData2.values()[0], axis=1)
    totalImage = numpy.append(totalImage, imageData3.values()[0], axis=1)
    totalImage = numpy.append(totalImage, imageData4.values()[0], axis=1)
    totalImage = numpy.append(totalImage, imageData5.values()[0], axis=1)
    totalImage = numpy.append(totalImage, imageData6.values()[0], axis=1)
    totalImage = numpy.append(totalImage, imageData7.values()[0], axis=1)

    #Save and show the file
    image = Image.fromarray(totalImage)
    image.save("plot" + str(i) + ".png")

def main():
    global zoom
    start = time.time()
    framestart = 0
    frameend = 650
    for x in range(framestart, frameend):
        start = time.time()
        zoom = 3/(1.05**x)
        createFrame(2,x)
        end = time.time()
        eta = (end-start)*(frameend-x)
        print("Frame " + str(x) + " of " + str(frameend) + " DONE! ETA: " + str(round(eta/60)) + " Minutes. This frame took: " + str(round(end-start)) + " seconds.", end = "\r")

    print("Movie completed")

if __name__ == '__main__':
    main()
