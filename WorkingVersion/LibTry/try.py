from enthought.traits.ui.api import FileEditor    
from traits.api \
    import HasTraits, File, Button

from traitsui.api \
    import View, HGroup, Item

save_file_editor = FileEditor(dialog_style='save')

class Files(HasTraits):
    filename_1 = File(exists=True)
    filename_2 = File(exists=True)

    traits_ui = View(
        Item('filename_1', editor=FileEditor()),
        Item('filename_2', editor=save_file_editor),
        title   = 'Select Geometry Files',
        buttons = ['OK', 'Cancel']
    )

files = Files()
ui = files.edit_traits(kind='modal')