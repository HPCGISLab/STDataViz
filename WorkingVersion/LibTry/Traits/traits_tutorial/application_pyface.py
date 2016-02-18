
#! The imports
#!-------------
#!
#! The MPLWidget is imported from last example.

from threading import Thread
from time import sleep
from enthought.traits import *
from enthought.pyface.api import SplitApplicationWindow, GUI
from enthought.traits.ui import View, Item, ButtonEditor, Group
from mplwidget import MPLWidget
from scipy import *

#! User interface objects
#!------------------------
#!
#! These objects store information for the program to interact with the
#! user via traitsUI.

class Experiment(HasTraits):
    """ Object that contains the parameters that control the experiment, 
        modified by the user.
    """
    width = Float(30, label="Width", desc="width of the cloud")
    x = Float(50, label="X", desc="X position of the center")
    y = Float(50, label="Y", desc="Y position of the center")


class Results(HasTraits):
    """ Object used to display the results.
    """
    width = Float(30, label="Width", desc="width of the cloud") 
    x = Float(50, label="X", desc="X position of the center")
    y = Float(50, label="Y", desc="Y position of the center")

    view = View( Item('width', style='readonly'),
                 Item('x', style='readonly'),
                 Item('y', style='readonly'),
               )

#!
#! The camera object also is a real object, and not only a data
#! structure: it has a method to acquire an image (or in our case
#! simulate acquiring), using its attributes as parameters for the
#! acquisition.
#!

class Camera(HasTraits):
    """ Camera objects. Implements both the camera parameters controls, and
        the picture acquisition.
    """
    exposure = Float(1, label="Exposure", desc="exposure, in ms")
    gain = Enum(1, 2, 3, label="Gain", desc="gain")

    def acquire(self, experiment):
       X, Y = indices((100, 100))
       Z = exp(-((X-experiment.x)**2+(Y-experiment.y)**2)/experiment.width**2)
       Z += 1-2*rand(100,100)
       Z *= self.exposure
       Z[Z>2] = 2
       Z = Z**self.gain
       return(Z)

#! Threads and flow control
#!--------------------------
#!
#! There are three threads in this application:
#! 
#!  * The GUI event loop, the only thread running at the start of the program.
#!
#!  * The acquisition thread, started through the GUI. This thread is an
#!    infinite loop that waits for the camera to be triggered, retrieves the 
#!    images, displays them, and spawns the processing thread for each image
#!    recieved.
#!
#!  * The processing thread, started by the acquisition thread. This thread
#!    is responsible for the numerical intensive work of the application.
#!    it processes the data and displays the results. It dies when it is done.
#!    One processing thread runs per shot acquired on the camera, but to avoid
#!    accumulation of threads in the case that the processing takes longer than
#!    the time lapse between two images, the acquisition thread checks that the
#!    processing thread is done before spawning a new one.
#! 

class AcquisitionThread(Thread):
    """ Acquisition loop. This is the worker thread that retrieves images 
        from the camera, displays them, and spawns the processing job.
    """
    wants_abort = False

    def process(self, image):
        """ Spawns the processing job.
        """
        try:
            if self.processing_job.isAlive():
                self.display("Processing to slow")
                return
        except AttributeError:
            pass
        self.processing_job = ProcessingJob()
        self.processing_job.image = image
        self.processing_job.results = self.results
        self.processing_job.start()

    def run(self):
        """ Runs the acquisition loop.
        """
        self.display('Camera started')
        n_img = 0
        while not self.wants_abort:
            n_img += 1
            img =self.acquire(self.experiment)
            self.display('%d image captured' % n_img)
            self.image_show(img)
            self.process(img)
            sleep(1)
        self.display('Camera stopped')

class ProcessingJob(Thread):
    """ This thread gets spawned each time data is acquired.
    """
    def run(self):
        im = self.image
        X, Y = indices(im.shape)
        x = sum(X*im)/sum(im)
        y = sum(Y*im)/sum(im)
        width = sqrt(abs(sum(((X-x)**2+(Y-y)**2)*im)/sum(im))) 
        GUI.invoke_later(setattr, self.results, 'x', x)
        GUI.invoke_later(setattr, self.results, 'y', y)
        GUI.invoke_later(setattr, self.results, 'width', width)

#! The GUI elements
#!------------------
#!
#! The GUI of this application is separated in two (and thus created by a
#! sub-class of *SplitApplicationWindow*).
#!
#! On the left a plotting area, made of an *MPLWidget* object, displays the 
#! images acquired by the camera.
#!
#! On the right a panel hosts the `TraitsUI` representation of a *ControlPanel*
#! object. This object is mainly a container for our other objects, but it also
#! has an *Button* for starting or stopping the acquisition, and a string 
#! (represented by a textbox) to display informations on the acquisition
#! process. The view attribute is tweaked to produce a pleasant and usable
#! dialog. Tabs are used as it help the display to be light and clear.
#!

class ControlPanel(HasTraits):
    """ This object is the core of the traitsUI interface. Its view is
        the right panel of the application, and it hosts the method for
        interaction between the objects and the GUI.
    """
    experiment = Instance(Experiment)
    camera = Instance(Camera)
    mplwidget = Instance(MPLWidget)
    results = Instance(Results)
    start_stop_acquisition = Button("Start/Stop acquisition")
    results_string =  String()
    acquisition_thread = Instance(AcquisitionThread)
    view = View(Group(
                Group(
                  Item('start_stop_acquisition', show_label=False ),
                  Item('results_string',show_label=False, 
                                        springy=True, style='custom' ),
                  label="Control"),
                Group(
                  Group(
                    Item('experiment', style='custom', show_label=False),
                    label="Input",),
                  Group(
                    Item('results', style='custom', show_label=False),
                    label="Results",),
                label='Experiment'),
                Item('camera', style='custom', show_label=False),
               layout='tabbed'),
               )

    def _start_stop_acquisition_fired(self):
        """ Callback of the "start stop acquisition" button. This starts
            the acquisition thread, or kills it/
        """
        if self.acquisition_thread and self.acquisition_thread.isAlive():
            self.acquisition_thread.wants_abort = True
        else:
            self.acquisition_thread = AcquisitionThread()
            self.acquisition_thread.display = self.add_line
            self.acquisition_thread.acquire = self.camera.acquire
            self.acquisition_thread.experiment = self.experiment
            self.acquisition_thread.image_show = self.image_show
            self.acquisition_thread.results = self.results
            self.acquisition_thread.start()
    
    def add_line(self, string):
        """ Adds a line to the textbox display in a thread-safe way.
        """
        GUI.invoke_later(setattr, self, 'results_string', 
                                (string + "\n" + self.results_string)[0:1000] )

    def image_show(self, image):
        """ Plots an image on the canvas in a thread safe way.
        """
        self.mplwidget.axes.images=[]
        self.mplwidget.axes.imshow(image, aspect='auto')
        GUI.invoke_later(self.mplwidget.figure.canvas.draw)


class MainWindow(SplitApplicationWindow):
    """ The main window, here go the instructions to create and destroy
        the application.
    """
    mplwidget = Instance(MPLWidget)
    panel = Instance(ControlPanel)
    ratio = Float(0.6)

    def _create_lhs(self, parent):
        self.mplwidget = MPLWidget(parent)
        return self.mplwidget.control

    def _create_rhs(self, parent):
        self.panel = ControlPanel(camera=Camera(), experiment=Experiment(),
                                mplwidget=self.mplwidget, results=Results())
        return self.panel.edit_traits(parent = parent, kind="subpanel").control

    def _on_close(self, event):
        if ( self.panel.acquisition_thread 
                            and self.panel.acquisition_thread.isAlive() ):
            self.panel.acquisition_thread.wants_abort = True
            while self.panel.acquisition_thread.isAlive():
                sleep(0.1)
        self.close()

if __name__ == '__main__':
    gui = GUI()
    window = MainWindow()
    window.size = (700, 400)
    window.open()
    gui.start_event_loop()
