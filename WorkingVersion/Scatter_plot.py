import numpy as np
from tvtk.api import tvtk
from mayavi.scripts import mayavi2


@mayavi2.standalone
def main():
    # Create some random points to view.
    pd = tvtk.PolyData()
    pd.points = np.random.random((1000, 3))
    verts = np.arange(0, 1000, 1)
    verts.shape = (1000, 1)
    pd.verts = verts
    pd.point_data.scalars = np.random.random(1000)
    pd.point_data.scalars.name = 'scalars'

    # Now visualize it using mayavi2.
    from mayavi.sources.vtk_data_source import VTKDataSource
    from mayavi.modules.outline import Outline
    from mayavi.modules.surface import Surface

    mayavi.new_scene()
    d = VTKDataSource()
    d.data = pd
    mayavi.add_source(d)
    mayavi.add_module(Outline())
    s = Surface()
    mayavi.add_module(s)
    s.actor.property.set(representation='p', point_size=2)
    # You could also use glyphs to render the points via the Glyph module.

if __name__ == '__main__':
    main()