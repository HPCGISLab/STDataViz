from threading import Thread
from time import sleep
from enthought.traits import *
from enthought.pyface.api import SplitApplicationWindow, GUI
from enthought.traits.ui import View, Item, ButtonEditor

class TextDisplay(HasTraits):
    string =  String()

    view= View( Item('string',show_label=False, springy=True, style='custom' ))

    def add_line(self, string):
        GUI.invoke_later(setattr, self, 'string', string + "\n" + self.string)

class CaptureThread(Thread):
    def run(self):
        self.display('Camera started')
        n_img = 0
        while not self.wants_abort:
            sleep(.5)
            n_img += 1
            self.display('%d image captured' % n_img)
        self.display('Camera stopped')

class Camera(HasTraits):
    start_stop_capture = Event()
    display = Instance(TextDisplay)
    capture_thread = Instance(CaptureThread)

    view = View( Item('start_stop_capture', editor=ButtonEditor(), 
                    show_label=False ))

    def _start_stop_capture_fired(self):
        if self.capture_thread and self.capture_thread.isAlive():
            self.capture_thread.wants_abort = True
        else:
            self.capture_thread = CaptureThread()
            self.capture_thread.wants_abort = False
            self.capture_thread.display = self.display.add_line
            self.capture_thread.start()

class MainWindow(SplitApplicationWindow):
    display = Instance(TextDisplay)
    camera = Instance(Camera)

    def _create_lhs(self, parent):
        self.display = TextDisplay()
        return self.display.edit_traits(parent = parent,
                            kind="subpanel").control
    def _create_rhs(self, parent):
        self.camera = Camera(display=self.display)
        return self.camera.edit_traits(parent = parent,
                            kind="subpanel").control


if __name__ == '__main__':
    gui = GUI()
    window = MainWindow()
    window.open()
    gui.start_event_loop()
