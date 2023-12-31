import os
import pytest
from data2firedrake import image2dat as i2d
import numpy as np
import firedrake as fd
from firedrake.petsc import PETSc


img_dir = os.path.dirname(__file__)
@pytest.mark.parametrize('img_path', [os.path.join(img_dir,'data','small_image_with_seven.png')])
@pytest.mark.parametrize('mesh_type', ['simplicial','cartesian'])
@pytest.mark.parametrize('normalizeRGB', [True, False])
@pytest.mark.parametrize('inverteBW', [True, False])
def test_convert_write(img_path, mesh_type, normalizeRGB, inverteBW):
    """
    Load an image and create a mesh
    image -> numpy -> firedrake function-> numpy -> image 
    Compare the results and assert equality.
    """
    # read and convert to matrix
    np_img = i2d.image2numpy(img_path,normalize=normalizeRGB,invert=inverteBW)
    
    # write back to file
    i2d.numpy2image(np_img,'image2numpy_and_back.png', normalized=normalizeRGB, inverted=inverteBW)
    
    # read and convert to matrix
    np_img2 = i2d.image2numpy('image2numpy_and_back.png',normalize=normalizeRGB,invert=inverteBW)
    fd.COMM_WORLD.Barrier()
    if fd.COMM_WORLD.Get_rank() == 0:
        os.remove('image2numpy_and_back.png')
    
    
    assert np.allclose(np_img,np_img2)
    
    # create mesh
    mesh = i2d.build_mesh_from_numpy(np_img, mesh_type=mesh_type)
    
    # convert to firedrake
    fire_img = i2d.numpy2firedrake(mesh, np_img, name='image')

    # convert to firedrake
    fire_img = i2d.numpy2firedrake(mesh, np_img, name='image')

    # convert back to numpy
    np_img_converted = i2d.firedrake2numpy(fire_img)

    # write to file
    i2d.numpy2image(np_img_converted,'test_load_image.png', normalized=normalizeRGB, inverted=inverteBW)
    

    # read stored image
    np_img2 = i2d.image2numpy('test_load_image.png', normalize=normalizeRGB, invert=inverteBW)
    fd.COMM_WORLD.Barrier()
    if fd.COMM_WORLD.Get_rank() == 0:
        os.remove('test_load_image.png')

    # compare saved and stored images
    assert np.allclose(np_img,np_img2)    

if __name__ == '__main__':
    img_path = os.path.join(img_dir,'data','small_image_with_seven.png')
    mesh_type = 'cartesian'
    normalizeRGB = True
    inverteBW = False
    test_convert_write(img_path, mesh_type, normalizeRGB, inverteBW)
