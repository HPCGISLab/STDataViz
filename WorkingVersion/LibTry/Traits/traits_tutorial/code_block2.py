from enthought.traits.api import *
from enthought.pyface.api import SplitApplicationWindow, GUI
from enthought.traits.ui.api import View, Item, ButtonEditor

class TextDisplay( HasTraits ):
    string =  String()

    view= View( Item('string',show_label=False, springy=True, style='custom' ))

class Camera( HasTraits):
    capture = Button()
    display = Instance(TextDisplay)

    view = View( Item('capture', show_label=False), )

    def _capture_fired(self):
        self.display.string += "Captured fired\n"

class MainWindow( SplitApplicationWindow ):
    display = Instance(TextDisplay)
    camera = Instance(Camera)

    def _create_lhs(self, parent):
        self.display = TextDisplay()
        return self.display.edit_traits(parent=parent,
                            kind="subpanel").control

    def _create_rhs(self, parent):
        self.camera = Camera(display=self.display)
        return self.camera.edit_traits(parent=parent,
                            kind="subpanel").control

if __name__ == '__main__':
    MainWindow().open()
    GUI().start_event_loop() 


