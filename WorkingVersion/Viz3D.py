# 3D Volume Graph and Backmap
# 2016/02/25
# Cheng Zhang (czhang0328@gmail.com)
# Class and functions in this file is modified from draw_volume.py

from os import listdir
from os.path import isfile, join, getmtime
import numpy as np
from mayavi import mlab
from pylab import imread
from GUILog import GUILog

# Default files
Default_dataDir='./ascfiles2'
Default_mapFile = './maps/worldmap.png'
Default_colorFile = './colormaps/color1.txt'

def load_data(dataDir):
    '''load all the data from files from one directory
    Parameters
    ----------
    fileDir : str
    Directory of the data files
       	    
    Returns
    -------
    3D np arry   
    '''
    dataDir = str(dataDir)
    x = []
    files = [join(dataDir,f) for f in listdir(dataDir) if isfile(join(dataDir,f)) ]
    for f in files:
        x.append(np.loadtxt(f,skiprows=6) )
       	        
    s = np.dstack(x)
    return s 
    
def read_color(filename):
    f = open(str(filename), "r")
    return [ [int(x) for x in lines.split(' ')] for lines in f ]
    
class File(object):
    def __init__(self, fileName):
        self.nameOld = fileName
        self.name = fileName
        self.mtime = getmtime(fileName)
    
    def __str__(self):
        return self.name
        
    def change_file(self,fileName):
        self.name = fileName
        self.mtime = getmtime(fileName)
        
    def if_changed(self):
        '''
        Only works when first time call
        '''
        curmtime = getmtime(self.name)
        if self.nameOld == self.name and self.mtime == curmtime:
            return True
        else:
            self.mtime = curmtime
            self.nameOld = self.name
            return False
        

class Viz3D(object):
    def __init__(self, mlab, m_log, dataDir=Default_dataDir,
                mapFile=Default_mapFile, colorFile=Default_colorFile):
        self.mlab = mlab
        self.dataDir = File(dataDir)
        self.mapFile = File(mapFile)
        self.colorFile = File(colorFile)
        self.log = m_log
             
    def draw_volume(self):
        ''' 3d Visualization of the data'''
        # Draw
        src = self.mlab.pipeline.scalar_field(self.data)
        src.update_image_data = True
        self.vol = self.mlab.pipeline.volume(src)
        self.mlab.axes(nb_labels=5, 
            ranges=(0,self.data.shape[0],0,self.data.shape[1],0,self.data.shape[2]))
        
    def draw_map(self):
        ''' Draw background map
        Note:Function must be called after load the volume data
        '''
        
        height = self.data.shape[0]
        width = self.data.shape[1]
        
        imageRGBData = imread(str(self.mapFile), format = 'png')
        imageGreyData = [ [sum(j) for j in i] for i in imageRGBData ]
        
        ims = self.mlab.imshow(imageGreyData,reset_zoom = False)
        ims.actor.position = [height/2,(width)/2,0]
        ims.actor.scale = [float(height)/len(imageGreyData),float(width)/len(imageGreyData[0]),0]

    def change_color_map(self):
        ''' Change color map of the volume figure
        '''
        # This warnings are just for test
        if self.data is None:
            self.log.add('Please choose the data file first')
            return
        if self.colormap is None:
            self.log.add('Please choose the colormap file first')
            return
        if self.vol is None:
            self.log.add('Please draw the data at least once')
            return
            
        # Changing the ctf:
        from tvtk.util.ctf import ColorTransferFunction
        ctf = ColorTransferFunction()
        for c in self.colormap:
            ctf.add_rgb_point(float(c[0]), float(c[1])/255.0, float(c[2])/255.0, float(c[3])/255.0)
        self.vol._volume_property.set_color(ctf)
        self.vol._ctf = ctf
        self.vol.update_ctf = True
    
        # Changing the otf
        from enthought.tvtk.util.ctf import PiecewiseFunction
        otf = PiecewiseFunction()
        for c in self.colormap:
            otf.add_point(float(c[0]), float(c[4])/255.0)
        self.vol._otf = otf
        self.vol._volume_property.set_scalar_opacity(otf)
        
    def draw(self):
        self.data = load_data(self.dataDir)
        self.colormap = read_color(self.colorFile)
        self.draw_volume()
        self.draw_map()
        self.change_color_map()
        
       		
def test():
    mlab.figure(bgcolor=(0,0,0), size=(800,800) )
    m_log = GUILog("Viz3D Test")
    viz = Viz3D(mlab,m_log)
    viz.draw()
    
if __name__ ==  '__main__':
    test()