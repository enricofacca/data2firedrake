import sys
import glob
import os
import numpy as np


from firedrake import *
from time import process_time
from otp import image2dat as i2d
import numpy as np
sys.path.append('../src/otp')
from utilities import save2pvd


# print('mesh 100')
# time = process_time()
# mesh = BoxMesh(nx=20,ny=20, 
#                         nz=20,  
#                         Lx=1, 
#                         Ly=1,
#                         Lz=1,
#                         hexahedral=True,
#                         )
# print('mesh 100',process_time()-time)



nx=4
ny=5
nz=7
example=np.zeros([nx,ny,nz])

x_array = np.linspace(1,nx+1,nx+1)[:-1]
y_array = np.linspace(nx+1,nx+ny+1,ny+1)[:-1]
z_array = np.linspace(nx+ny+1,nx+ny+nz+1,nz+1)[:-1]



example[:,0,0] = x_array[:]
example[0,:,0] = y_array[:]
example[0,0,:] = z_array[:]

#example = np.arange(nx*ny*nz).reshape([nx,ny,nz])

lengths = [1,1,1]
mesh = i2d.build_mesh_from_numpy(example, mesh_type='cartesian',lengths=lengths)
#print('simpelx?', mesh.ufl_cell().is_simplex())
source_fire = i2d.numpy2firedrake(mesh, example, 'source',lengths=lengths)
save2pvd(source_fire, 'source.pvd')
