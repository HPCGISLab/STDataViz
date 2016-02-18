from enthought.traits import *
from enthought.pyface.api import SplitApplicationWindow, GUI
from enthought.traits.ui import View, Item, ButtonEditor

class TextDisplay( HasTraits ):
    string =  String()

    view= View( Item('string',show_label=False, springy=True, style='custom' ))

class Camera( HasTraits):
    capture = Event()
    display = Instance(TextDisplay)

    view = View( Item('capture', editor=ButtonEditor() ))

    def _capture_fired(self):
        self.display.string += "Captured fired\n"

class Container(HasTraits):
     camera = Instance(Camera)
     display = Instance(TextDisplay)

     view = View(
                 Item('camera', style='custom', show_label=False, ),
                 Item('display', style='custom', show_label=False, ),
                )

display = TextDisplay()
container = Container(camera = Camera(display=display), display = display)

container.configure_traits()
 

