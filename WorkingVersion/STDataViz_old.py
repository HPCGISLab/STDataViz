# -*- coding: utf-8 -*-
from mayavi import mlab
from traits.api import HasTraits, Range, Instance, \
        on_trait_change, Array, Str, Directory, Button, File, List
from traitsui.api import View, Item, HSplit, Group, VSplit
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor
from mayavi.core.api import PipelineBase
from enthought.traits.ui.menu import NoButtons
from traitsui.api import TableEditor, ObjectColumn, TableColumn

from draw_volume import loadData, drawVolume, changeVolumeColormap, \
        drawMap, readColorFile, changeToBestView
from time import time
        
# Default Values
def_dataDir = "./ascfiles2"
def_mapFile = "./maps/worldmap.png"
def_colorFile = "./colormaps/color1.txt" 

    

class ControlPanel(HasTraits):
    dataDir = Directory(value = def_dataDir, exist = True)
    mapFile = File(value = def_mapFile,exist = True, filter=["*.png"])
    colorFile = File(value = def_colorFile, exist = True)
    log = Str("--- STDataViz (Last Modify: 02/18/16) ---\n\n")
    
    volume = Instance(PipelineBase)
    
    runButton = Button("Run")
    
    colormap = List()
    
    colorButton = Button("Change")
    
    view = View(VSplit(
                    Group(
                        Group(
                            Item('dataDir',style='simple'),
                            Item('mapFile',style='simple'),
                            Item('colorFile',style='simple'),
                            Item('runButton', show_label=False),
                            label = 'Setting', dock='tab'),
                        Group(
                            Item('colormap',show_label=False,
                                editor = TableEditor(
                                    columns=[TableColumn(),
                                    TableColumn()]) ),
                            Item('colorButton', show_label=False),
                            label = 'Colormap', dock='tab'),
                        layout = 'tabbed'
                    ),
                    Group(
                        Item('log', style='custom', show_label=False),
                    )
                )
            )
            
    @on_trait_change('dataDir')
    def update_dataDir(self):
        self.dataDirChanged = True
        
    @on_trait_change('mapFile')
    def update_mapFile(self):
        self.mapFileChanged = True
        
    @on_trait_change('colorFile')
    def update_colorFile(self):
        self.colorFileChanged = True
        
    
    def _colorButton_fired(self):
        print self.colormap
        changeVolumeColormap(self.volume,self.colormap)
        self.colorFileChanged = False
        self.log += "Updated Colormap.\n"
            
    def _runButton_fired(self):
        if self.dataDir == "" or self.mapFile=="" or self.colorFile=="":
            self.log += "Please Complete the upper part.\n"
        else:
            start_time = time()
            if self.volume is None:
                # Disable Render to save calculate
                self.scene.disable_render = True
                # Set Background to black
                self.scene.background = (0,0,0)
                
                # Load Data
                self.data = loadData(self.dataDir)
                # Draw Background Map
                self.map = drawMap(self.mlab, self.data, self.mapFile)
                changeToBestView(self.mlab)
                
                # Draw 3d volume graph
                self.volume = drawVolume(self.mlab,self.data)
                self.colormap = readColorFile(self.colorFile)
                changeVolumeColormap(self.volume,self.colormap)
                changeToBestView(self.mlab)
                
                # Enable Render
                self.scene.disable_render = False
                
                # For Update 
                self.dataDirChanged = False
                self.mapFileChanged = False
                self.colorFileChanged = False
                
                self.log += "Created 3d visualization\n"
            else:
                # Change 3d volume graph
                if self.dataDirChanged:
                    self.data = loadData(self.dataDir)
                    self.mlab_source.set(scalars = self.data)
                    self.dataDirChanged = False
                    self.log += "Updated 3d data.\n"
                
                # Change Color Map
                elif self.colorFileChanged:
                    self.colormap = readColorFile(self.colorFile)
                    changeVolumeColormap(self.volume,self.colormap)
                    self.colorFileChanged = False
                    self.log += "Updated Colormap.\n"
                    
                # Change Background Map
                elif self.mapFileChanged:
                    self.map.remove()
                    self.map = drawMap(self.mlab, self.data, self.mapFile)
                    changeToBestView(self.mlab)
                    self.mapFileChanged = False
                    self.log += "Updated Background Map.\n"
                    
                else:
                    self.log += "Nothing Changed\n"
            
            self.log += "Work Done. Used %.3f seconds \n\n" %(time()-start_time)
    
class STDataViz(HasTraits):
    # Left Side Figure Scene
    scene = Instance(MlabSceneModel, args=( )  )
    # Control Panel
    panel = Instance(ControlPanel)
    # Sync with Control Panel
    volume = Instance(PipelineBase)
    
    def _panel_default(self):
        return ControlPanel(volume=self.volume, mlab=self.scene.mlab,
                scene = self.scene)
        
    view = View(
                HSplit(
                    Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                                height=500, width=700, show_label=False),
                    Item('panel',style='custom'),
                    show_labels = False,
                ),
                resizable=True,
                height=0.75, width=0.75,
            )

if __name__ == '__main__':
    viz = STDataViz()
    viz.configure_traits()
