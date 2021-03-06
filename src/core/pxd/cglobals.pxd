'''
Author: Víctor Ruiz Gómez
Description: This file will declare all the methods and classes defined in the lib3d
mec ginac globals.h that will be used by this library
'''



######## Imports ########

from src.core.pxd.ginac.cexpr cimport ex
from src.core.pxd.ginac.clst  cimport lst
from src.core.pxd.cmatrix     cimport Matrix
from src.core.pxd.cvector3D   cimport Vector3D
from src.core.pxd.ctensor3D   cimport Tensor3D
from src.core.pxd.cwrench3D   cimport Wrench3D




######## Global functions and variables ########

cdef extern from "Globals.h":
    bint atomization
    bint gravity


    # Unatomization
    ex unatomize(ex)
    Matrix unatomize(Matrix)
    Vector3D unatomize(Vector3D)
    Tensor3D unatomize(Tensor3D)
    Wrench3D unatomize(Wrench3D)
    
    # Atomization   
    ex atomize_ex(ex)
    
    # Substitution
    Matrix subs(Matrix, Matrix, float)

    # Matrix list opimization
    void matrix_list_optimize(Matrix&, lst&, lst&)
