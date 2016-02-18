from enthought.traits.api import *
from enthought.traits.ui.api import View, Handler, Item
from threading import Thread
import wx
from time import sleep

class MyThread(Thread):
    wants_abort = False

    def run(self):
        self.display('Started')
        while not self.wants_abort:
            self.display('Running')
            sleep(1)
        self.display('Camera stopped')


class MainWindowHandler(Handler):
    def close(self, info, is_OK):
        if ( info.object.thread and info.object.thread.isAlive() ):
            info.object.thread.wants_abort = True
            while info.object.thread.isAlive():
                sleep(0.1)
            #wx.Yield()
        return True


class MainWindow(HasTraits):
    thread = False
    start_stop_thread = Button()
    results_string =  String()

    def add_line(self, string):
        self.results_string = (string + "\n" + self.results_string)[0:1000]

    def _start_stop_thread_fired(self):
        if self.thread and self.thread.isAlive():
            self.thread.wants_abort = True
        else:
            self.thread = MyThread()
            self.thread.display = self.add_line
            self.thread.start()

    view = View(Item('results_string', style='custom'), 
                    'start_stop_thread',
                    handler=MainWindowHandler(), 
                    resizable=True)

if __name__ == '__main__':
    MainWindow().configure_traits()
