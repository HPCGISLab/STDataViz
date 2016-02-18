#other traits imports
from traits.api \
    import HasTraits, File, Button

from traitsui.api \
    import View, VGroup, HGroup, Item
from pyface.api import FileDialog
class FileDialogDemo(HasTraits):
    file_name = File
    openTxt = Button('Open...')
    traits_view = View( 
        VGroup( 
            HGroup(
              Item( 'openTxt', show_label = False ),
              '_',
              Item( 'file_name', style = 'readonly', width = 200 ),
            ),
        )
        )
    def _openTxt_fired(self):
        """ Handles the user clicking the 'Open...' button.
        """
        extns = ['*.png',]#seems to handle only one extension...
        wildcard='|'.join(extns)

        dialog = FileDialog(title='Select file',
            action='open', wildcard=wildcard,
             default_path = self.file_name)
        if dialog.open() == True:
            self.file_name = dialog.path
            self.openFile(dialog.path)     
    def openTxtFile(self, path):
        'do something'
        print path
    
# Create the demo:
demo = FileDialogDemo()

# Run the demo (if invoked from the command line):
if __name__ == '__main__':
    demo.configure_traits()