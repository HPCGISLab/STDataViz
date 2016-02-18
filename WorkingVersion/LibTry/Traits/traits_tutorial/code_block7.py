from enthought.traits.api import Any, Instance, Float, Str
try:
    from enthought.pyface.api import SplitApplicationWindow, PythonShell, GUI, \
            PythonEditor
except ImportError:
    from enthought.pyface import SplitApplicationWindow, PythonShell, GUI, \
            PythonEditor

class MainWindow(SplitApplicationWindow):

    shell = Instance(PythonShell)
    editor =  Instance(PythonEditor)

    ratio = Float(0.5)
    direction = Str('horizontal')

    def _create_lhs(self, parent):
        self.editor = PythonEditor(parent)
        return self.editor.control

    def _create_rhs(self, parent):
        shell = self.shell = PythonShell(parent)
        return self.shell.control

window = MainWindow()
window.open()
window.size = (600, 200)
GUI().start_event_loop()

