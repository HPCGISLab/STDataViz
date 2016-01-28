# 3D Volume Graph using Mayavi
# 2015-09-09
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

filedir='/Users/czhang/Desktop/Mayavi/ascfiles2/'

# read meta data from the first 6 line of the asc file
def metadataforfile(filename):
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

# read data from one file
def filedataforfile(filenum):
    filename=filedir+"tmp_kdeout"+str(filenum)+".asc"
    nparr=np.loadtxt(filename, skiprows=6)
    return nparr

# load all the data from files and return 3d matrix
def loadData():
    x = []
    onlyfiles = [ f for f in listdir(filedir) if isfile(join(filedir,f)) ]
    zlength=len(onlyfiles)
    for i in xrange(zlength):
        filedat=filedataforfile(i)
        x.append(filedat)
    y=np.dstack(x)
    print "3d shape", y.shape
    return y  

# change the ctf and otf property of volume
def change_volume_property(vol):
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
    
    color = color2
    
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
    
    
def change_test(vol):
    from enthought.tvtk.util.ctf import PiecewiseFunction
    otf = PiecewiseFunction()
    otf.add_point(0, 0)
    otf.add_point(1000,1)
    vol._otf = otf
    vol._volume_property.set_scalar_opacity(otf)
    
# draw volume
def draw_volume(scalars):
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
    fig = mlab.figure(bgcolor=(0,0,0), size=(800,800) )
    src = mlab.pipeline.scalar_field(scalars)
    src.update_image_data = True
    #src.spacing = [1, 1, 1]
    
    vol = mlab.pipeline.volume(src)
    
    change_volume_property(vol)
    #change_test(vol)
    
    #vol = mlab.pipeline.image_plane_widget(src,plane_orientation='z_axes', slice_index=shape[2]/2)
    ax = mlab.axes(nb_labels=5, ranges=(0,shape[0],0,shape[1],0,shape[2]))
    
    mlab.savefig("result.jpg")
    print "nmax =", nmax
    print "nmin =", nmin
    
    viewkeeper = mlab.view()
    print "View", mlab.view()
    draw_map(shape[0],shape[1])
    mlab.view(viewkeeper[0],viewkeeper[1],viewkeeper[2],viewkeeper[3])
    
def draw_map(height,width):
    im = pl.imread('./maps/worldmap_Miller_cylindrical_projection.png', format='png')
    im = pl.imread('./maps/worldmap.png', format='png')
    #im = pl.imread('./maps/worldmap2.png', format='png')
    
    l = []
    for i in im:
        x = []
        for j in i:
            tmp = 0
            for k in j: tmp += k
            x.append(tmp)
        l.append(x)
    print im
    ims = mlab.imshow(l, colormap = 'binary')
    print "Map shape", len(l),len(l[0])
    
    ims.actor.position = [height/2,(width)/2,0]
    ims.actor.scale = [float(height)/len(l),float(width)/len(l[0]),0]


def main():
    import pylab as pl
    s = loadData()
    draw_volume(s)
    
if __name__ == "__main__":
    main()