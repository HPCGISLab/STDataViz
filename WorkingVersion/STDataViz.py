from mayavi import mlab
from traits.api import HasTraits, Range, Instance, \
        on_trait_change, Array, Str, Directory, Button, File
from traitsui.api import View, Item, HSplit, Group
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor
from mayavi.core.api import PipelineBase
from enthought.traits.ui.menu import NoButtons

from draw_volume import loadData, drawVolume, changeVolumeColormap, \
        drawMap, readColorFile, changeToBestView
        
# Default Values
def_dataDir = "./ascfiles2"
def_mapFile = "./maps/worldmap.png"
def_colorFile = "./colormaps/color1.txt"

class ControlPanel(HasTraits):
    dataDir = Directory(value = def_dataDir, exist = True)
    mapFile = File(value = def_mapFile,exist = True)
    colorFile = File(value = def_colorFile, exist = True)
    
    
    volume = Instance(PipelineBase)
    
    runButton = Button("Run")
    view = View(Group(
                    Group(
                        Item('dataDir',style='simple'),
                        Item('mapFile',style='simple'),
                        Item('colorFile',style='simple'),
                        Item('runButton', show_label=False),
                        label = 'Setting', dock='tab'
                    ),
                    layout = 'tabbed'
                ),
                resizable = True
            )
            
    def _runButton_fired(self):
        if self.dataDir != "" and self.mapFile!="" and self.colorFile!="":
            if self.volume is None:
                self.scene.disable_render = True
                self.scene.background = (0,0,0)
                self.data = loadData(self.dataDir)
                self.map = drawMap(self.mlab, self.data, self.mapFile)
                changeToBestView(self.mlab)
                self.volume = drawVolume(self.mlab,self.data)
                colormap = readColorFile(self.colorFile)
                changeVolumeColormap(self.volume,colormap)
                changeToBestView(self.mlab)
                self.scene.disable_render = False
            else:
                
                colormap = readColorFile(self.colorFile)
                changeVolumeColormap(self.volume,colormap)
                self.scene.disable_render = True
                self.map.remove()
                self.map = drawMap(self.mlab, self.data, self.mapFile)
                changeToBestView(self.mlab)
                self.scene.disable_render = False
    
class STDataViz(HasTraits):
    
    scene = Instance(MlabSceneModel, args=( )  )
    
    panel = Instance(ControlPanel)
    
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
