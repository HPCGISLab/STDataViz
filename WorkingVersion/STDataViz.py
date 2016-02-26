# -*- coding: utf-8 -*-
from mayavi import mlab
from traits.api import HasTraits, Range, Instance, \
        on_trait_change, Array, Str, Directory, Button, File, List
from traitsui.api import View, Item, HSplit, Group, VSplit
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor
from mayavi.core.api import PipelineBase
from enthought.traits.ui.menu import NoButtons
from traitsui.api import TableEditor, ObjectColumn, TableColumn
from time import time

from GUILog import GUILog
from Viz3D import Viz3D
        
# Default Values
def_dataDir = "./ascfiles2"
def_mapFile = "./maps/worldmap.png"
def_colorFile = "./colormaps/color1.txt" 


class ControlPanel(HasTraits):
    viz = Instance(Viz3D)
    dataDir = Directory(value = viz.dataDir, exist = True)
    #mapFile = File(value = viz.mapFile,exist = True, filter=["*.png"])
    #colorFile = File(value = viz.colorFile, exist = True)
    runButton = Button("Run")
    
    alphaTable = List()
    
    view = View(Group(Group(Item('dataDir',style='simple'),
                    #Item('mapFile', style='simple'),
                    #Item('colorFile',style='simple'),
                    Item('runButton', show_label=False),
                    label = 'Setting', dock='tab'),
                Group(Item('alphaTable', show_label=False),
                    label = 'Change Alpha Value', dock='tab'),
                layout = 'tabbed'))
    
    def _runButton_fired(self):
        self.log.add("viz.dataDir")
                
                    
    
class STDataViz(HasTraits):
    # Left Side Figure Scene
    scene = Instance(MlabSceneModel, args=( )  )
    # Control Panel
    panel = Instance(ControlPanel)
    # Log Panel
    log = value = GUILog("STDataViz (Last Modify: 02/25/2016)")
    # Viz3D
    viz = Instance(Viz3D)
    def _viz_default(self):
        return Viz3D(self.scene.mlab, self.log)
    
    def _panel_default(self):
        return ControlPanel(viz = self.viz,scene = self.scene, log=self.log)
        
    view = View(
                HSplit(
                    Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                                width=0.7, show_label=False),
                    VSplit(
                        Item('panel',style='custom'),
                        Item('log',style='custom',height=0.63),
                        show_labels = False),
                    show_labels = False,
                ),
                resizable=True,height=0.8, width=0.8,
            )

if __name__ == '__main__':
    viz = STDataViz()
    viz.configure_traits()
