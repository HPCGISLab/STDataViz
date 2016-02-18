# 3D Volume Graph using Mayavi
# 2016/02/18
# By Jay and Cheng
# This program reads ascfiles from 'filedir', creates 3d matrix,
# uses mayavi display the 3d matrix, and also saves a screenshot in 
# the working directory.
# Notice: Files must be in some format, and the filedir must be specified

from os import listdir
from os.path import isfile, join
import fileinput
import numpy as np
from mayavi import mlab
import pylab as pl

def metadataforfile(filename,filedir):
    '''read meta data from the first 6 line of the asc file
    '''
    metadata=[None]*6
    nrows=ncols=None
    x=y=None
    cellsize=None
    nodata_value=None
    print filedir+filename
    for line in fileinput.input([filedir+filename]):
        
        arg, val = str.split(line)
        print arg, val
        if arg == "nrows":
            nrows = int(val)
            metadata[0]=nrows
        if arg == "ncols":
            ncols = int(val)
            metadata[1]=ncols
        if arg == "xllcorner":
            x = float(val)
            metadata[3]=x
        if arg == "yllcorner":
            y = float(val)
            metadata[4]=y
        if arg == "cellsize":
            cellsize=float(val)
            metadata[2]=cellsize
        if arg == "NODATA_value":
            nodata_value=float(val)
            metadata[5]=nodata_value
        if fileinput.filelineno()>=6:
            break
    fileinput.close()
    return metadata


def loadData(fileDir):
    '''load all the data from files from one directory
    Parameters
    ----------
    fileDir : str
        Directory of the data files
    
    Returns
    -------
    3d np arry   
    '''
    x = []
    files = [join(fileDir,f) for f in listdir(fileDir) if isfile(join(fileDir,f)) ]
    for f in files:
        x.append(np.loadtxt(f,skiprows=6) )
        
    y=np.dstack(x)

    print "3d shape", y.shape
    return y  


def changeVolumeColormap(vol,color):
    '''change the ctf and otf property of volume
    Parameters
    ----------
    vol : mlab.volume
    color : [[]]
        For each color [datavalue, R, G, B, A]
        R,G,B,A in range(0.0,255.0) inclusive
    '''
    
    # Changing the ctf:
    from tvtk.util.ctf import ColorTransferFunction
    ctf = ColorTransferFunction()
    for c in color:
        ctf.add_rgb_point(c[0], c[1]/255.0, c[2]/255.0, c[3]/255.0)
    vol._volume_property.set_color(ctf)
    vol._ctf = ctf
    vol.update_ctf = True

    # Changing the otf
    from enthought.tvtk.util.ctf import PiecewiseFunction
    otf = PiecewiseFunction()
    for c in color:
        otf.add_point(c[0], c[4]/255.0)
    vol._otf = otf
    vol._volume_property.set_scalar_opacity(otf)
    
    
def changeTest(vol):
    ''' Test for vol change
    '''
    from enthought.tvtk.util.ctf import PiecewiseFunction
    otf = PiecewiseFunction()
    otf.add_point(0, 0)
    otf.add_point(1000,1)
    vol._otf = otf
    vol._volume_property.set_scalar_opacity(otf)
    
def drawVolume(mlab,scalars):
    ''' 3d Visualization of the data
    Parameters
    ----------
    mlab : mlab
    scalars : 3d np array
    
    Returns
    -------
    volume object
    '''
    # filts out low data
    nmax = np.amax(scalars)
    nmin = np.amin(scalars)
    #nptp = nmax - nmin
    #lowBound = nmin + nptp*0
    #for i in np.nditer(scalars, op_flags=['readwrite']):
    #    if i<lowBound: i[...] = 0
    
    # Get the shape of axes
    shape = scalars.shape
    
    # draw
    src = mlab.pipeline.scalar_field(scalars)
    src.update_image_data = True
    #src.spacing = [1, 1, 1]
    
    vol = mlab.pipeline.volume(src)
    
    #vol = mlab.pipeline.image_plane_widget(src,plane_orientation='z_axes', slice_index=shape[2]/2)
    ax = mlab.axes(nb_labels=5, ranges=(0,shape[0],0,shape[1],0,shape[2]))
    
    mlab.savefig("result.jpg")
    print "nmax =", nmax
    print "nmin =", nmin
    viewkeeper = mlab.view()
    print "View", mlab.view()
    mlab.view(viewkeeper[0],viewkeeper[1],viewkeeper[2],viewkeeper[3])
    return vol
    
def drawMap(mlab, scalars, mapFile):
    ''' 3d Visualization of the data
    Parameters
    ----------
    mlab : mlab
    scalars : 3d np array
    mapFile : str
    
    Returns
    -------
    imshow object
    '''
    # Get the shape of axes
    shape = scalars.shape
    height = shape[0]
    width = shape[1]
    
    im = pl.imread(mapFile, format = 'png')
    
    l = []
    for i in im:
        x = []
        for j in i:
            tmp = 0
            for k in j: tmp += k
            x.append(tmp)
        l.append(x)
        
    #ims = mlab.imshow(l, colormap = 'binary')
    ims = mlab.imshow(l)
    print "Map shape", len(l),len(l[0])
    
    ims.actor.position = [height/2,(width)/2,0]
    ims.actor.scale = [float(height)/len(l),float(width)/len(l[0]),0]
    
    return ims

def changeToBestView(mlab):
    mlab.view(45.0, 54.735610317245346, 1477.5179822379857, [ 147. ,  352.5,   38. ])

def readColorFile(filename):
    f = open(filename, "r")
    return [ [float(x) for x in lines.split(' ')] for lines in f ]

def main():
    fileDir='./ascfiles2'
    mapFile = './maps/worldmap.png'
    colorFile = './colormaps/color1.txt'

    # color map used for test
    color1 = [[0,0,0,0,0],
        [1,255,255,0,10],
        [10,255,255,0,50],
        [100,255,100,0,150],
        [1000,255,0,0,255]]
    
    color2 = [[0,0,0,0,0],
        [100,0,255,255,10],
        [1000,0,255,255,50],
        [10000,0,100,255,150],
        [100000,0,0,255,255]]

    s = loadData(fileDir)
    mlab.figure(bgcolor=(0,0,0), size=(800,800) )
    vol = drawVolume(mlab,s)
    colormap = readColorFile(colorFile)
    changeVolumeColormap(vol,colormap)
    drawMap(mlab, s, mapFile)
    changeToBestView(mlab)
    
if __name__ == "__main__":
    main()