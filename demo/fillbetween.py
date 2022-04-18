import os
from sys import argv
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import csv



import numpy as np
import pylab as plt

def rect(x,y,w,h,c):
    ax = plt.gca()
    polygon = plt.Rectangle((x,y),w,h,color=c)
    ax.add_patch(polygon)


def wavelength_to_rgb(wavelength, gamma=0.8):

    '''This converts a given wavelength of light to an 
    approximate RGB color value. The wavelength must be given
    in nanometers in the range from 380 nm through 750 nm
    (789 THz through 400 THz).

    Based on code by Dan Bruton
    http://www.physics.sfasu.edu/astro/color/spectra.html
    '''

    wavelength = float(wavelength)
    if wavelength >= 380 and wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif wavelength >= 440 and wavelength <= 490:
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif wavelength >= 490 and wavelength <= 510:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif wavelength >= 510 and wavelength <= 580:
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif wavelength >= 580 and wavelength <= 645:
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif wavelength >= 645 and wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0
    #R *= 255
    #G *= 255
    #B *= 255
    #return (int(R), int(G), int(B))
    return (R,G,B)


def rainbow_fill(X,Y):
    plt.plot(X,Y,lw=0)  # Plot so the axes scale correctly

    dx = X[1]-X[0]
    N  = float(X.size)

    for n, (x,y) in enumerate(zip(X,Y)):
        color = wavelength_to_rgb(x)
        #color = cmap(n/N)
        rect(x,0,dx,y,color)



def main(argv):
    # fig params
    fig = mpl.pyplot.figure(figsize=(7,5))
    ax1 = fig.add_subplot(111)
    
    cx = []; cy = []; x = []; y = [];
    i = 0
    lw = 2
    Cx = 1; Cy = 1 # convert 
    c1 = "mediumblue"; c2 = "forestgreen"; cfill = "magenta"; trans=0.15
    for file in argv:
        print("Reading file " + file + "...")
        if(i == 0):
            print("Starting script")
        elif(i == 1):
            # load the hysteresis as calibration curve
            with open(file,'r') as csvfile:
                plots = csv.reader(csvfile, delimiter = '\t')
                next(plots)
                for row in plots:
                    if(float(row[0])%2 == 0):
                        cx.append(float(row[0]))
                        cy.append(float(row[1]))
            print("Length of s1:" + str(len(cx)))
            plt.plot(cx,cy,c=c1,label="Chip #1",lw=lw)
        else:
            x = []; y = [];
            with open(file,'r') as csvfile:
                plots = csv.reader(csvfile, delimiter = '\t')
                next(plots)
                #while (row == None) in next(plots):
                for j in range(600):
                    try:
                        row = next(plots)
                    except:
                        break
                    if(float(row[0])%2 == 0):
                        x.append(float(row[0]))
                        y.append(float(row[1]))
                    #y.append(float(row[1]))
            print("Length of s2:" + str(len(x)))
            plt.plot(x,y,c=c2,label="Chip #2",lw=lw)
            #ax1.fill_between(x,0,y, color="black")
            #ax1.fill_between(x,0,cy, color="black")
            ax1.fill_between(x,y,cy, color=cfill, alpha=trans)
            #ax1.fill_between(x,y,cy,where=(cy > y), color="green")
        i += 1  
    # show all the plots
    # optionally, save figure
    #rainbow_fill(np.array(cx),np.array(cy))
    #ax1.set_title("C", fontname="Arial", fontsize=15)
    ax1.set_ylabel("Transmission ratio", fontname="Arial", fontsize=15)
    ax1.set_xlabel("Wavelength (nm)", fontname="Arial", fontsize=15)
    #plt.xlim(400,750)
    #plt.grid()
    #fig.colorbar(surface, shrink=0.5, aspect=5, ticks = tickLt)
    #plt.savefig("$file.png")
    ax1.legend()
    plt.show()


main(argv)



