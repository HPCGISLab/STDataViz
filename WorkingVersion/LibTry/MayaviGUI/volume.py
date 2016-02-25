import numpy as np
x, y, z = np.ogrid[-10:10:20j, -10:10:20j, -10:10:20j]
s = np.sin(x*y*z)/(x*y*z)

from mayavi import mlab
mlab.figure(bgcolor=(1, 1, 1))
mlab.pipeline.volume(mlab.pipeline.scalar_field(s))